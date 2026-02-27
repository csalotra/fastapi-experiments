from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, Band, BandCreate, BandWithID

app = FastAPI()

BANDS = [
  {"id": 1, "name": "The Beatles", "genre": "Rock"},
  {"id": 2, "name": "The Rolling Stones" , "genre": "Electronic", "albums": [ {"title": "Master of Reality", "release_date": "1971-05-01"} ]},{
  "id": 3, "name": "Led Zeppelin", "genre": "Rock"},
  {"id": 4, "name": "Pink Floyd", "genre": "Progressive Rock"},
  {"id": 5, "name": "Queen", "genre": "Hip-Hop"},
]

@app.get('/')
async def index() -> dict[str,str]:
  return {"hello": "world"}


@app.get("/about")
async def about() -> str:
  return "An Exceptional Company"


@app.get("/bands")
async def bands() -> list[Band]:
  return [
    Band(**b) for b in BANDS
  ]


@app.get("/bands/{band_id}")
async def band(band_id: int) -> Band:
  band = next((Band(**b) for b in BANDS if b["id"] == band_id), None)

  if band is None:
    raise HTTPException(status_code=404, detail="Band not found")
  return band


# Path parameter with Enum validation
@app.get("/bands/genre/{genre}")
async def bands_by_genre(genre: GenreURLChoices) -> list[dict]:
  return [b for b in BANDS if b["genre"].lower() == genre.value.lower()]

# Query parameter with Enum validation
@app.get('/bands_with_genre')
async def bamds_by_genre_query(
  genre: GenreURLChoices| None = None,
  has_albums: bool = False                         
) -> list[BandWithID]:
  
  band_list = [BandWithID(**b) for b in BANDS]
  if genre:
    band_list = [b for b in band_list if b.genre.value.lower() == genre.value.lower()]
  if has_albums:
    band_list = [b for b in band_list if len(b.albums) > 0]
  return band_list


@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandWithID:
  id = BANDS[-1]["id"] + 1
  band = BandWithID(id=id, **band_data.model_dump()).model_dump()
  BANDS.append(band)
  return band
