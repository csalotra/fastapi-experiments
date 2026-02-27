from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date

class GenreURLChoices(Enum):
  ROCK = "rock"
  ELECTRONIC = "electronic"
  PROGRESSIVE_ROCK = "progressive rock"
  HIP_HOP = "hip-hop"

class GenreChoices(Enum):
  ROCK = "Rock"
  ELECTRONIC = "Electronic"
  PROGRESSIVE_ROCK = "Progressive Rock"
  HIP_HOP = "Hip-Hop"


class Album(BaseModel):
  title: str
  release_date: date

class Band(BaseModel):
  id: int
  name: str
  genre: str
  albums: list[Album] = []   #default value for albums is an empty list

class BandBase(BaseModel):
  name: str
  genre: GenreChoices
  albums: list[Album] = []

# The field validator is used to ensure that the genre field is always stored in title case, regardless of how it's inputted. This helps maintain consistency in the data.
class BandCreate(BandBase):
  @field_validator("genre", mode="before")
  def title_case_genre(cls, v):
      if isinstance(v, str):
          return v.title()
      return v

class BandWithID(BandBase):
  id: int



