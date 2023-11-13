from dataclasses import dataclass
from typing import List


@dataclass
class PlayerCstat:
    name: str
    points: float
    total_time: float
    human_time: float
    zombie_time: float
    zombie_kills: int
    zombie_hs: int
    infected: int
    items_picked: int
    boss_killed: int
    leader_count: int
    td_count: int

    def __init__(self, raw_text: List[str]):
        for line in raw_text:
            parts = line.split(":", 1)

            if len(parts) != 2:
                print(line, "does not fit expected format")
                raise Exception

            if parts[0] == "cStat Details":
                self.name = parts[1].strip()
            elif parts[0] == "Points":
                self.points = float(parts[1])
            elif parts[0] == "Total Time":
                self.total_time = PlayerCstat.time_convert(parts[1])
            elif parts[0] == "Human Time":
                self.human_time = PlayerCstat.time_convert(parts[1])
            elif parts[0] == "Zombie Time":
                self.zombie_time = PlayerCstat.time_convert(parts[1])
            elif parts[0] == "Zombies Killed":
                self.zombie_kills = int(parts[1])
            elif parts[0] == "Zombies Killed (HS)":
                self.zombie_hs = int(parts[1])
            elif parts[0] == "Infected":
                self.infected = int(parts[1].rstrip(" players"))
            elif parts[0] == "Items picked up":
                self.items_picked = int(parts[1])
            elif parts[0] == "Boss Killed":
                self.boss_killed = int(parts[1])
            elif parts[0] == "Leader Count":
                self.leader_count = int(parts[1])
            elif parts[0] == "TopDefender Count":
                self.td_count = int(parts[1])
            else:
                print(parts[0], "does not match a case")
                raise Exception
            
    def time_convert(timestring: str) -> float:
        splitstring = timestring.split(" ")
        splitstring.pop(0)
        days = 0.0
        hours = 0.0
        minutes = 0.0
        seconds = 0.0
        for part in splitstring:
            if "d" in part:
                days = int(part.rstrip("d"))
            elif "h" in part:
                hours = int(part.rstrip("h"))
            elif "m" in part:
                minutes = int(part.rstrip("m"))
            elif "s" in part:
                seconds = int(part.rstrip("s"))

        time = days + (hours / 24) + (minutes / 1440 ) + (seconds / 86400)
        return time