import csv
import os
from typing import List, Dict, Any

class MovieManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.movies = self._load_movies()

    def _load_movies(self) -> List[Dict[str, Any]]:
        """
        Load movies from CSV file
        
        Returns:
            List of movie dictionaries
        """
        if not os.path.exists(self.filename):
            print(f"Error: File {self.filename} not found!")
            return []

        movies = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    movies.append(row)
        except Exception as e:
            print(f"Error reading file: {e}")
        
        return movies

    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Search movies by name (case-insensitive, partial match)
        
        Args:
            name: Search query for movie name
        
        Returns:
            List of matching movies
        """
        name = name.lower()
        return [
            movie for movie in self.movies 
            if name in movie['title'].lower()
        ]

    def search_by_year(self, year: int) -> List[Dict[str, Any]]:
        """
        Search movies by release year
        
        Args:
            year: Release year to search
        
        Returns:
            List of movies released in the specified year
        """
        return [
            movie for movie in self.movies 
            if movie['release_year'] == str(year)
        ]

    def search_by_director(self, director: str) -> List[Dict[str, Any]]:
        """
        Search movies by director (case-insensitive, partial match)
        
        Args:
            director: Search query for director name
        
        Returns:
            List of movies directed by the specified name
        """
        director = director.lower()
        return [
            movie for movie in self.movies 
            if director in movie['director'].lower()
        ]

    def display_movies(self, movies: List[Dict[str, Any]]) -> None:
        """
        Display movie details
        
        Args:
            movies: List of movies to display
        """
        if not movies:
            print("\n🎬 No movies found.")
            return

        print("\n🎬 Movie Search Results:")
        print("-" * 50)
        for movie in movies:
            print(f"Title: {movie['title']}")
            print(f"Year: {movie['release_year']}")
            print(f"Director: {movie['director']}")
            print("-" * 50)

def main():
    # Ensure CSV file exists in the same directory
    filename = 'movies.csv'
    
    # Create movie manager instance
    movie_manager = MovieManager(filename)

    while True:
        # Display menu
        print("\n🎥 Movie Data Management System")
        print("1. Search Movie by Name")
        print("2. Search Movie by Release Year")
        print("3. Search Movie by Director")
        print("4. Exit")

        try:
            # Get user choice
            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == '1':
                # Search by name
                name = input("Enter movie name: ").strip()
                results = movie_manager.search_by_name(name)
                movie_manager.display_movies(results)

            elif choice == '2':
                # Search by year
                try:
                    year = int(input("Enter release year: ").strip())
                    results = movie_manager.search_by_year(year)
                    movie_manager.display_movies(results)
                except ValueError:
                    print("Invalid year. Please enter a valid number.")

            elif choice == '3':
                # Search by director
                director = input("Enter director name: ").strip()
                results = movie_manager.search_by_director(director)
                movie_manager.display_movies(results)

            elif choice == '4':
                # Exit the application
                print("Exiting Movie Management System. Goodbye! 👋")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
