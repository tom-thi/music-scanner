from dataclasses import dataclass

@dataclass
class TrackSplitSettings:
    # duration in seconds of every segment that is analyzed
    segment_duration_in_s: float = 5.0
    # gaps between the segments to not be analyzed
    gap_duration_in_s: float = 120.0
