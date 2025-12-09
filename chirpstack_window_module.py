import os
import pandas as pd

def summarize_chirpstack_windows(
    input_file: str,
    output_file: str = None,
    window_seconds: int | None = 30,
) -> str:
    """
    Summarizes ChirpStack Join-request and Uplink (Confirmed/Unconfirmed data up).

    window_seconds:
        - > 0 : group messages in fixed-size windows of that many seconds
        - None or <= 0 : no bucketing, each timestamp (floored to second) is its own window
    """
    # If no output file given, create "summary_<input-filename>" in same directory
    if output_file is None:
        in_dir = os.path.dirname(input_file)          # e.g. "Data"
        in_base = os.path.basename(input_file)        # e.g. "mqtt_data_20251202_120000.csv"
        output_file = os.path.join(in_dir, f"summary_{in_base}")
        # => "Data/summary_mqtt_data_20251202_120000.csv"

    # Load input CSV
    df = pd.read_csv(input_file)
    if df.empty:
        empty = pd.DataFrame(
            columns=["DevEUI", "Device_address", "Time_Window_Start", "Join_Request_Count", "Uplink_Data_Count"]
        )
        empty.to_csv(output_file, index=False)
        return output_file

    # Parse and sort timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        empty = pd.DataFrame(
            columns=["DevEUI", "Device_address", "Time_Window_Start", "Join_Request_Count", "Uplink_Data_Count"]
        )
        empty.to_csv(output_file, index=False)
        return output_file

    df = df.sort_values("timestamp")

    # Normalize MType and classify messages
    df["MType"] = df["MType"].astype(str).str.strip().str.lower()
    df["is_join"] = df["MType"].eq("join-request")
    df["is_uplink"] = df["MType"].isin(["confirmed data up", "unconfirmed data up"])

    # Build windows
    if window_seconds is not None and window_seconds > 0:
        # Fixed-size windows from earliest timestamp
        t0 = df["timestamp"].min()
        df["window_start"] = t0 + pd.to_timedelta(
            ((df["timestamp"] - t0).dt.total_seconds() // window_seconds).astype(int) * window_seconds,
            unit="s",
        )
    else:
        # No bucketing: each timestamp floored to second is its own "window"
        df["window_start"] = df["timestamp"].dt.floor("S")

    # Helper to join unique non-empty values
    def join_unique(values):
        vals = values.dropna().tolist()
        vals = [str(v).strip() for v in vals if str(v).strip().lower() != "nan" and str(v).strip() != ""]
        seen = []
        for v in vals:
            if v not in seen:
                seen.append(v)
        return "-".join(seen) if seen else ""

    # Group by window
    summary = (
        df.groupby("window_start")
          .agg(
              Join_Request_Count=("is_join", "sum"),
              Uplink_Data_Count=("is_uplink", "sum"),
              DevEUI=("DevEUI", join_unique),
              Device_address=("Device_address", join_unique),
          )
          .reset_index()
    )

    # Only windows with at least one relevant message
    summary = summary[(summary["Join_Request_Count"] > 0) | (summary["Uplink_Data_Count"] > 0)]

    if summary.empty:
        empty = pd.DataFrame(
            columns=["DevEUI", "Device_address", "Time_Window_Start", "Join_Request_Count", "Uplink_Data_Count"]
        )
        empty.to_csv(output_file, index=False)
        return output_file

    # Format time as "1:36:19 pm"
    summary["Time_Window_Start"] = summary["window_start"].dt.strftime("%I:%M:%S %p")
    summary["Time_Window_Start"] = (
        summary["Time_Window_Start"]
        .str.replace(r"^0", "", regex=True)
        .str.replace("AM", "am")
        .str.replace("PM", "pm")
    )

    # Reorder columns
    summary = summary[["DevEUI", "Device_address", "Time_Window_Start", "Join_Request_Count", "Uplink_Data_Count"]]

    summary.to_csv(output_file, index=False)
    return output_file
