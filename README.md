# DiceAndTiles-Backend
recommendation microservice: https://github.com/MScha99/FastAPI-recommendation/tree/main  
data-fetching microservice: https://github.com/MScha99/FastAPI-scrapper

This is a back-end web app for a board game catalog and collection management system, built with **Django** and **PostgreSQL**. Built with a microservice architecture in mind, this service manages users' collections and communicates with other services via API calls. bIt allows users to browse, rate, and comment on board games while also managing their personal collections. A recommendation system suggests new games based on user preferences.

## Features of the entire system (incl other services):
- **Game Catalog**: Browse all board games with filtering by name.
- **User Accounts**: Register and log in to manage personal collections and reviews.
- **Game Reviews**: Users can rate and comment on games.
- **Collection Management**: Add and remove games from a personal collection.
- **Recommendations**: ML-driven recommendations based on user preferences.
- **Data Fetching**: Integration with external board game databases.

## Endpoints
Full API documentation available at: https://boardgamecollection.docs.apiary.io/

### **Product Service**
- `GET /products` - Retrieve all products.
- `POST /vote` - Submit a rating for a product.
- `POST /comment` - Submit a comment on a product.
- `POST /ownedproduct` - Add a game to a user's collection.

### **User Authentication**
- `POST /register` - Register a new user.
- `POST /login` - Authenticate user.

### **Recommendation Service**
- `GET /recommend` - Get game recommendations based on the current product.

### **Fetching Service**
- `POST /fetch` - Retrieve and process board game data from BoardGameGeek.
- `POST /insert` - Store processed data in the database.
- `GET /fetchedproducts` - Retrieve processed product data.

## Installation
This app includes Docker support for easy deployment, and includes pgadmin4 for easy db overview:

1. Install Docker/Docker Desktop.
2. Run `docker compose up` in the terminal.
3. Access the app at `http://localhost:8000/`.

#

![ERD kontenery](https://github.com/user-attachments/assets/f9c558a2-52bd-4049-89ee-cd24ff554237)
> Database entity relationship diagram (ERD)

