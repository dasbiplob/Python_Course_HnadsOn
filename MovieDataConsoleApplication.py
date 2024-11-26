from dataclasses import dataclass
from typing import List, Optional, Callable, Dict, Any
from functools import lru_cache
import csv
import os
from abc import ABC, abstractmethod
import logging
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import threading
from collections import defaultdict
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SearchCriteria(Enum):
    TITLE = "title"
    YEAR = "release_year"
    DIRECTOR = "director"

@dataclass(frozen=True)
class Movie:
    """Immutable movie data class with hash support for caching"""
    title: str
    release_year: int
    director: str

    def __hash__(self):
        return hash((self.title, self.release_year, self.director))

class SearchStrategy(ABC):
    """Abstract base class for search strategies"""
    @abstractmethod
    def search(self, movies: List[Movie], query: Any) -> List[Movie]:
        pass

class TitleSearchStrategy(SearchStrategy):
    def search(self, movies: List[Movie], query: str) -> List[Movie]:
        query = query.lower()
        return [movie for movie in movies if query in movie.title.lower()]

class YearSearchStrategy(SearchStrategy):
    def search(self, movies: List[Movie], query: int) -> List[Movie]:
        return [movie for movie in movies if movie.release_year == query]

class DirectorSearchStrategy(SearchStrategy):
    def search(self, movies: List[Movie], query: str) -> List[Movie]:
        query = query.lower()
        return [movie for movie in movies if query in movie.director.lower()]

class MovieDataSource:
    """Handle data loading and caching"""
    def __init__(self, filename: str):
        self.filename = filename
        self._movies: Optional[List[Movie]] = None
        self._last_modified: float = 0
        self._lock = threading.Lock()
        self._index: Dict[str, Dict[str, List[Movie]]] = defaultdict(lambda: defaultdict(list))

    @property
    def movies(self) -> List[Movie]:
        """Thread-safe lazy loading with file modification check"""
        current_mtime = os.path.getmtime(self.filename)
        
        with self._lock:
            if self._movies is None or current_mtime > self._last_modified:
                self._load_movies()
                self._last_modified = current_mtime
            
            return self._movies

    def _load_movies(self) -> None:
        """Load and index movies from CSV"""
        logger.info(f"Loading movies from {self.filename}")
        try:
            movies = []
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movie = Movie(
                        title=row['title'],
                        release_year=int(row['release_year']),
                        director=row['director']
                    )
                    movies.append(movie)
            
            self._movies = movies
            self._build_index()
            
        except Exception as e:
            logger.error(f"Error loading movies: {str(e)}")
            raise

    def _build_index(self) -> None:
        """Build search indices for better performance"""
        self._index.clear()
        
        # Index by year
        for movie in self._movies:
            self._index['year'][str(movie.release_year)].append(movie)
            
        # Index by director
        for movie in self._movies:
            self._index['director'][movie.director.lower()].append(movie)

class MovieManager:
    """Main movie management class with caching and search strategies"""
    def __init__(self, filename: str):
        self.data_source = MovieDataSource(filename)
        self._search_strategies = {
            SearchCriteria.TITLE: TitleSearchStrategy(),
            SearchCriteria.YEAR: YearSearchStrategy(),
            SearchCriteria.DIRECTOR: DirectorSearchStrategy()
        }

    @lru_cache(maxsize=128)
    def search(self, criteria: SearchCriteria, query: Any) -> List[Movie]:
        """Cached search with strategy pattern"""
        strategy = self._search_strategies[criteria]
        return strategy.search(self.data_source.movies, query)

class ConsoleUI:
    """Separate UI concerns"""
    def __init__(self, movie_manager: MovieManager):
        self.movie_manager = movie_manager

    @staticmethod
    def display_movies(movies: List[Movie]) -> None:
        if not movies:
            print("\nNo movies found.")
            return

        print("\nSearch Results:")
        print("-" * 50)
        for movie in movies:
            print(f"Title: {movie.title}")
            print(f"Year: {movie.release_year}")
            print(f"Director: {movie.director}")
            print("-" * 50)

    def run(self) -> None:
        while True:
            try:
                print("\nMovie Data Management")
                print("1. Search Movie by Name")
                print("2. Search Movie by Release Year")
                print("3. Search Movie by Director")
                print("4. Exit")

                choice = input("\nEnter your choice (1-4): ").strip()

                if choice == '4':
                    print("Exiting application.")
                    break

                if choice == '1':
                    query = input("Enter movie name: ").strip()
                    results = self.movie_manager.search(SearchCriteria.TITLE, query)
                
                elif choice == '2':
                    year = int(input("Enter release year: ").strip())
                    results = self.movie_manager.search(SearchCriteria.YEAR, year)
                
                elif choice == '3':
                    query = input("Enter director name: ").strip()
                    results = self.movie_manager.search(SearchCriteria.DIRECTOR, query)
                
                else:
                    print("Invalid choice. Please try again.")
                    continue

                self.display_movies(results)

            except ValueError as e:
                print(f"Invalid input: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                print("An unexpected error occurred. Please try again.")

def main():
    try:
        filename = 'movies.csv'
        movie_manager = MovieManager(filename)
        ui = ConsoleUI(movie_manager)
        ui.run()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        print("Error starting application. Check the logs for details.")

if __name__ == "__main__":
    main()
