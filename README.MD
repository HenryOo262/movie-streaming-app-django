# Movie Streaming App - Django

Movie Streaming Website developed as a Semester VI CS-205 Web Development with Python project at UCSY.

## MovWave

This is a movie streaming website using Django as a backend with SQLite3 and Firebase.

## Identified Bugs

+ Comment deletion is not working as expected

+ Actor info css is not responsive

## Setting Up The Project 

### Firebase Console

In firebase console paste this in Storage/Rules -

service firebase.storage {
  match /b/video-stream-app-6b509.appspot.com/o {
    match /{allPaths=**} {
      // Allow access by all users
      allow read, write;
    }
  }
}

Create folders named movies, series, posters in the bucket.

### Project Directory 

Create folder named firebase at the root.

Place the firebase service account JSON file in the firebase folder.

Terminal :

pip install firebase-admin
