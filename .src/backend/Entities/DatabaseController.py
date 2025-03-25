import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import uuid
from typing import List, Optional, Dict, Any, Union

# Import entities
from Entities.User import User
from Entities.Activity import Activity
from Entities.Route import Route
from Entities.Location import Location
from Entities.SavedRoutes import SavedRoutes
from Entities.Settings import Settings
from Entities.Filters import Filters

class DatabaseController:
    """Firebase Firestore database controller for the cycling application.
    
    This class provides methods to interact with the Firestore database,
    handling CRUD operations for all application entities.
    """
    
    def __init__(self):
        """Initialize the database connection"""
        cred = credentials.Certificate(".src/backend/work.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    # User methods
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieves a user by their ID.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            User object if found, None otherwise
        """
        user_doc = self.db.collection('usernames').document(user_id).get()
        if user_doc.exists:
            data = user_doc.to_dict()
            
            # Get user settings
            settings = Settings()
            settings._user_id = user_id
            settings._email = data.get('email', '')
            settings._password = data.get('password', '')
            settings._app_notifications = data.get('notification_enabled', True)
            
            # Create user with basic info
            user = User(
                user_id=user_id,
                email=data.get('email', ''),
                password=data.get('password', '')
            )
            
            # Set user settings
            user.settings = settings
            
            # Get user filters
            filters = Filters()
            filters_data = data.get('filters', {})
            filters._show_water_point = filters_data.get('show_water_point', False)
            filters._show_repair_shop = filters_data.get('show_repair_shop', False)
            user.filters = filters
            
            return user
        return None
    
    def username_exists(self, username: str) -> bool:
        """Checks if a username is already taken.
        
        Args:
            username: Username to check
            
        Returns:
            True if username exists
        """
        users = self.db.collection('users').where('username', '==', username).get()
        return len(users) > 0
    
    def email_exists(self, email: str) -> bool:
        """Checks if an email is already registered.
        
        Args:
            email: Email to check
            
        Returns:
            True if email exists
        """
        users = self.db.collection('users').where('email', '==', email).get()
        return len(users) > 0
    
    def add_user(self, user: User) -> bool:
        """Adds a new user to the database.
        
        Args:
            user: User object to add
            
        Returns:
            True if successful
        """
        try:
            # Create basic user document
            user_data = {
                'email': user.email,
                'password': user.password,
                'notification_enabled': user.settings._app_notifications if user.settings else True
            }
            
            self.db.collection('users').document(user.user_id).set(user_data)
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_user(self, user: User) -> bool:
        """Updates an existing user's information.
        
        Args:
            user: User object with updated data
            
        Returns:
            True if successful
        """
        try:
            # Update basic user document
            user_data = {
                'email': user.email,
                'password': user.password,
                'notification_enabled': user.settings._app_notifications if user.settings else True
            }
            
            self.db.collection('users').document(user.user_id).update(user_data)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def update_user_profile_picture(self, user_id: str, profile_picture: bytes) -> bool:
        """Updates a user's profile picture.
        
        Args:
            user_id: User identifier
            profile_picture: Binary image data
            
        Returns:
            True if successful
        """
        try:
            # In a real implementation, you'd upload this to Firebase Storage
            # and store the URL in Firestore. For simplicity, we'll just mock this.
            self.db.collection('users').document(user_id).update({
                'has_profile_picture': True
            })
            return True
        except Exception as e:
            print(f"Error updating profile picture: {e}")
            return False
    
    # Activity methods
    def add_activity(self, activity: Activity) -> bool:
        """Adds a new activity to the database.
        
        Args:
            activity: Activity object to add
            
        Returns:
            True if successful
        """
        try:
            # Create activity document
            activity_data = {
                'user_id': activity.user.user_id,
                'date_time_started': activity.date_time_started,
                'date_time_ended': activity.date_time_ended,
                'time_elapsed': activity.get_time_elapsed(),
            }
            
            # Add route data if available
            if activity.route_taken:
                route = activity.route_taken
                activity_data['route'] = {
                    'start_point': {
                        'location_id': route.start_point.location_id,
                        'latitude': route.start_point.latitude,
                        'longitude': route.start_point.longitude,
                        'address': route.start_point.address
                    },
                    'end_point': {
                        'location_id': route.end_point.location_id,
                        'latitude': route.end_point.latitude,
                        'longitude': route.end_point.longitude,
                        'address': route.end_point.address
                    }
                }
            
            # Generate new activity ID if not set
            if not activity.activity_id:
                activity.activity_id = str(uuid.uuid4())
            
            # Add to database
            self.db.collection('activities').document(str(activity.activity_id)).set(activity_data)
            
            # Update user's activities list
            user_ref = self.db.collection('users').document(activity.user.user_id)
            user_ref.update({
                'activity_ids': firestore.ArrayUnion([str(activity.activity_id)])
            })
            
            return True
        except Exception as e:
            print(f"Error adding activity: {e}")
            return False
    
    def get_user_activities(self, user_id: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[Activity]:
        """Retrieves activities for a user with optional filtering.
        
        Args:
            user_id: User identifier
            period: Time period filter ('week', 'month', 'year' or None)
            limit: Maximum number of activities to return
            
        Returns:
            List of Activity objects
        """
        try:
            # Create query
            query = self.db.collection('activities').where('user_id', '==', user_id)
            
            # Apply time period filter
            if period:
                cutoff_date = datetime.now()
                if period == 'week':
                    cutoff_date -= timedelta(days=7)
                elif period == 'month':
                    cutoff_date -= timedelta(days=30)
                elif period == 'year':
                    cutoff_date -= timedelta(days=365)
                
                query = query.where('date_time_started', '>=', cutoff_date)
            
            # Order by date (newest first)
            query = query.order_by('date_time_started', direction=firestore.Query.DESCENDING)
            
            # Apply limit if specified
            if limit:
                query = query.limit(limit)
            
            # Execute query
            activities_data = query.get()
            
            # Get user
            user = self.get_user_by_id(user_id)
            if not user:
                return []
            
            # Create Activity objects
            activities = []
            for doc in activities_data:
                data = doc.to_dict()
                
                # Create Activity
                activity = Activity(activity_id=doc.id, user=user)
                activity.date_time_started = data.get('date_time_started')
                activity.date_time_ended = data.get('date_time_ended')
                activity.time_elapsed = data.get('time_elapsed')
                
                # Add route if available
                route_data = data.get('route')
                if route_data:
                    start_data = route_data.get('start_point', {})
                    end_data = route_data.get('end_point', {})
                    
                    start_point = Location(
                        location_id=start_data.get('location_id', 0),
                        lat=start_data.get('latitude', 0),
                        lng=start_data.get('longitude', 0),
                        address=start_data.get('address', '')
                    )
                    
                    end_point = Location(
                        location_id=end_data.get('location_id', 0),
                        lat=end_data.get('latitude', 0),
                        lng=end_data.get('longitude', 0),
                        address=end_data.get('address', '')
                    )
                    
                    route = Route(start_point=start_point, end_point=end_point)
                    activity.set_route_taken(route)
                
                activities.append(activity)
            
            return activities
        except Exception as e:
            print(f"Error getting user activities: {e}")
            return []
    
    def delete_activity(self, user_id: str, activity_id: str) -> bool:
        """Deletes an activity from the database.
        
        Args:
            user_id: User identifier
            activity_id: Activity identifier
            
        Returns:
            True if successful
        """
        try:
            # Check if activity belongs to user
            activity_ref = self.db.collection('activities').document(activity_id)
            activity_doc = activity_ref.get()
            
            if not activity_doc.exists:
                return False
            
            if activity_doc.to_dict().get('user_id') != user_id:
                return False
            
            # Delete activity
            activity_ref.delete()
            
            # Update user's activities list
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({
                'activity_ids': firestore.ArrayRemove([activity_id])
            })
            
            return True
        except Exception as e:
            print(f"Error deleting activity: {e}")
            return False
    
    # Route methods
    def get_route(self, route_id: str) -> Optional[Route]:
        """Retrieves a route by its ID.
        
        Args:
            route_id: Unique route identifier
            
        Returns:
            Route object if found, None otherwise
        """
        try:
            route_doc = self.db.collection('routes').document(route_id).get()
            
            if not route_doc.exists:
                return None
            
            data = route_doc.to_dict()
            
            # Create start location
            start_data = data.get('start_point', {})
            start_point = Location(
                location_id=start_data.get('location_id', 0),
                lat=start_data.get('latitude', 0),
                lng=start_data.get('longitude', 0),
                address=start_data.get('address', '')
            )
            
            # Create end location
            end_data = data.get('end_point', {})
            end_point = Location(
                location_id=end_data.get('location_id', 0),
                lat=end_data.get('latitude', 0),
                lng=end_data.get('longitude', 0),
                address=end_data.get('address', '')
            )
            
            # Create route
            route = Route(start_point=start_point, end_point=end_point)
            
            return route
        except Exception as e:
            print(f"Error getting route: {e}")
            return None
    
    def add_route(self, route: Route) -> str:
        """Adds a new route to the database.
        
        Args:
            route: Route object to add
            
        Returns:
            Route ID if successful, empty string otherwise
        """
        try:
            # Create route document
            route_data = {
                'start_point': {
                    'location_id': route.start_point.location_id,
                    'latitude': route.start_point.latitude,
                    'longitude': route.start_point.longitude,
                    'address': route.start_point.address
                },
                'end_point': {
                    'location_id': route.end_point.location_id,
                    'latitude': route.end_point.latitude,
                    'longitude': route.end_point.longitude,
                    'address': route.end_point.address
                }
            }
            
            # Add to database
            route_ref = self.db.collection('routes').document()
            route_ref.set(route_data)
            
            return route_ref.id
        except Exception as e:
            print(f"Error adding route: {e}")
            return ""
    
    def add_recent_search(self, user_id: str, route: Route) -> bool:
        """Records a recent route search for a user.
        
        Args:
            user_id: User identifier
            route: Route that was searched
            
        Returns:
            True if successful
        """
        try:
            # Add route first
            route_id = self.add_route(route)
            if not route_id:
                return False
            
            # Add to recent searches
            recent_search_data = {
                'route_id': route_id,
                'timestamp': firestore.SERVER_TIMESTAMP
            }
            
            self.db.collection('users').document(user_id).collection('recent_searches').document(route_id).set(recent_search_data)
            
            # Get all recent searches to limit to 5
            recent_searches_ref = self.db.collection('users').document(user_id).collection('recent_searches')
            recent_searches = recent_searches_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).get()
            
            # Keep only the 5 most recent
            if len(recent_searches) > 5:
                for i, doc in enumerate(recent_searches):
                    if i >= 5:
                        doc.reference.delete()
            
            return True
        except Exception as e:
            print(f"Error adding recent search: {e}")
            return False
    
    def get_recent_searches(self, user_id: str, limit: int = 5) -> List[Route]:
        """Retrieves a user's recent route searches.
        
        Args:
            user_id: User identifier
            limit: Maximum number of searches to return
            
        Returns:
            List of Route objects
        """
        try:
            # Get recent searches
            recent_searches_ref = self.db.collection('users').document(user_id).collection('recent_searches')
            recent_searches = recent_searches_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).get()
            
            routes = []
            for doc in recent_searches:
                route_id = doc.to_dict().get('route_id')
                route = self.get_route(route_id)
                if route:
                    routes.append(route)
            
            return routes
        except Exception as e:
            print(f"Error getting recent searches: {e}")
            return []
    
    # Facility methods
    def get_facilities(self, facility_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves facilities from the database with optional filtering.
        
        Args:
            facility_type: Filter by facility type (None for all)
            
        Returns:
            List of facility dictionaries
        """
        try:
            # Create query
            query = self.db.collection('facilities')
            
            # Apply type filter
            if facility_type:
                query = query.where('type', '==', facility_type)
            
            # Execute query
            facilities_data = query.get()
            
            # Create facility dictionaries
            facilities = []
            for doc in facilities_data:
                data = doc.to_dict()
                data['id'] = doc.id
                facilities.append(data)
            
            return facilities
        except Exception as e:
            print(f"Error getting facilities: {e}")
            return []
    
    # SavedRoutes methods
    def get_saved_routes(self, user_id: str) -> List[SavedRoutes]:
        """Retrieves a user's saved routes.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of SavedRoutes objects
        """
        try:
            # Get saved routes collection
            saved_routes_ref = self.db.collection('users').document(user_id).collection('saved_routes')
            saved_routes_data = saved_routes_ref.get()
            
            # Create SavedRoutes objects
            saved_routes = []
            for doc in saved_routes_data:
                data = doc.to_dict()
                
                # Get route details
                route_id = data.get('route_id')
                route = self.get_route(route_id)
                
                if route:
                    # Calculate distance (mock implementation)
                    start = route.start_point
                    end = route.end_point
                    distance = self._calculate_distance(
                        start.latitude, start.longitude, 
                        end.latitude, end.longitude
                    )
                    
                    # Create SavedRoutes object
                    saved_route = SavedRoutes(
                        route_name=data.get('name', f"Route {doc.id}"),
                        distance=distance
                    )
                    
                    # Set additional attributes
                    saved_route.average_time_taken = data.get('average_time_taken', 0)
                    saved_route.number_of_rides = data.get('number_of_rides', 0)
                    
                    saved_routes.append(saved_route)
            
            return saved_routes
        except Exception as e:
            print(f"Error getting saved routes: {e}")
            return []
    
    def save_route(self, user_id: str, route: Route, name: str = "") -> bool:
        """Saves a route for a user.
        
        Args:
            user_id: User identifier
            route: Route to save
            name: Optional name for saved route
            
        Returns:
            True if successful
        """
        try:
            # Add route first
            route_id = self.add_route(route)
            if not route_id:
                return False
            
            # Calculate distance
            start = route.start_point
            end = route.end_point
            distance = self._calculate_distance(
                start.latitude, start.longitude, 
                end.latitude, end.longitude
            )
            
            # Create saved route entry
            saved_route_data = {
                'route_id': route_id,
                'name': name if name else f"Route {route_id[:8]}",
                'distance': distance,
                'average_time_taken': 0,
                'number_of_rides': 0,
                'timestamp': firestore.SERVER_TIMESTAMP
            }
            
            self.db.collection('users').document(user_id).collection('saved_routes').document(route_id).set(saved_route_data)
            
            return True
        except Exception as e:
            print(f"Error saving route: {e}")
            return False
    
    def unsave_route(self, user_id: str, route_id: str) -> bool:
        """Removes a saved route for a user.
        
        Args:
            user_id: User identifier
            route_id: Route identifier
            
        Returns:
            True if successful
        """
        try:
            # Delete saved route entry
            self.db.collection('users').document(user_id).collection('saved_routes').document(route_id).delete()
            
            return True
        except Exception as e:
            print(f"Error unsaving route: {e}")
            return False
    
    # Filter methods
    def update_filters(self, user_id: str, filters: Filters) -> bool:
        """Updates a user's map filters.
        
        Args:
            user_id: User identifier
            filters: Filters object with updated preferences
            
        Returns:
            True if successful
        """
        try:
            # Create filters document
            filters_data = {
                'show_water_point': filters.get_water_point(),
                'show_repair_shop': filters._show_repair_shop  # Using private attribute directly as get method isn't defined
            }
            
            # Update user's filters
            self.db.collection('users').document(user_id).update({
                'filters': filters_data
            })
            
            return True
        except Exception as e:
            print(f"Error updating filters: {e}")
            return False
    
    # Settings methods
    def update_notification_settings(self, user_id: str, notification_enabled: bool) -> bool:
        """Updates a user's notification preferences.
        
        Args:
            user_id: User identifier
            notification_enabled: True to enable notifications
            
        Returns:
            True if successful
        """
        try:
            # Update user's notification settings
            self.db.collection('users').document(user_id).update({
                'notification_enabled': notification_enabled
            })
            
            return True
        except Exception as e:
            print(f"Error updating notification settings: {e}")
            return False
    
    # Helper methods
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates distance between two coordinates using Haversine formula.
        
        Args:
            lat1: Latitude of first point
            lon1: Longitude of first point
            lat2: Latitude of second point
            lon2: Longitude of second point
            
        Returns:
            Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2
        
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        r = 6371  # Radius of Earth in kilometers
        
        return r * c