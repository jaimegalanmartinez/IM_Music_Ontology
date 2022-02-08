# IM_Music_Ontology

## Importing songs with Spotify API

- Visit https://developer.spotify.com/console/get-several-tracks/ to acquire a `user-read-private` token
- Copy the token to `api/.token.secret`
- Call `api/import-user-songs.py`
- Append individuals to the ontology by ` >> musicOntology_G3.owl` (Use `git restore` to revert)
