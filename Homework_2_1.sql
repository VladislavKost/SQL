CREATE TABLE IF NOT EXISTS genres (
	genre_id serial PRIMARY KEY,  
	genre_name varchar(50) NOT NULL
 	);  
 
CREATE TABLE IF NOT EXISTS singers (
	singer_id serial PRIMARY KEY,
 	singer_name varchar(50) NOT NULL 
 	);
    
CREATE TABLE IF NOT EXISTS singers_genres (
 	singer_id int REFERENCES singers(singer_id),  
 	genre_id  int REFERENCES genres(genre_id),
 	PRIMARY KEY (singer_id, genre_id) 
 	);  
 
CREATE TABLE IF NOT EXISTS albums (
	album_id serial PRIMARY KEY,  
	album_name varchar(50) NOT NULL,
	release_date date NOT NULL  
 	);
 
CREATE TABLE singers_albums (
	album_id  int REFERENCES albums(album_id),  
	singer_id int REFERENCES singers(singer_id),
 	PRIMARY KEY (album_id, singer_id)  
 	);   
  
CREATE TABLE songs (
	song_id serial primary key,  
	song_name varchar(50) NOT NULL,
	duration numeric NULL,  
	album_id int NOT NULL REFERENCES albums(album_id) 
 	);  
  
CREATE TABLE collections (
	collection_id serial PRIMARY KEY,  
	collection_name varchar(50) NOT NULL,
	release_date date NOT NULL  
 	); 

CREATE TABLE collections_songs (
	collection_id  int REFERENCES collections(collection_id),  
	song_id int REFERENCES songs(song_id),
	PRIMARY KEY (collection_id, song_id)  
	); 
  
