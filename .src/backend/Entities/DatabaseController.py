import firebase_admin
import firebase_admin.firestore
import pyrebase
import uuid
import os
from pathlib import Path
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Union
from flask import jsonify

# Import entities
from Entities.User import User
from Entities.Activity import Activity
from Entities.Route import Route
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
        self.db = firestore.client()
    
    # User methods

    def get_user_document(self, uid: str) -> Optional[Dict[str, Any]]:
        """Retrieves a user document by user ID.
        
        Args:
            uid: Unique user identifier
            
        Returns:
            User document if found, None otherwise
        """
        user_doc = self.db.collection('users').document(uid).get()
        if user_doc.exists:
            return user_doc
        return None

    def get_email_by_username(self, username: str) -> Optional[str]:
        """Retrieves an email address by username.
        
        Args:
            username: Username to search for
            
        Returns:
            Email address if found, None otherwise
        """
        user_doc = self.db.collection('usernames').document(username).get()
        if user_doc.exists:
            return user_doc.to_dict().get('email')
        return None

    def get_username_by_uid(self, uid: str) -> Optional[str]:
        """Retrieves a username by user ID.
        
        Args:
            uid: Unique user identifier
            
        Returns:
            Username if found, None otherwise
        """
        user_doc = self.db.collection('users').document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict().get('username')
        return None

    def get_uid_by_username(self, username: str) -> Optional[str]:
        """Retrieves a user's unique identifier by their username.
        
        Args:
            username: Username to search for
            
        Returns:
            User ID if found, None otherwise
        """
        user_doc = self.db.collection('usernames').document(username).get()
        if user_doc.exists:
            return user_doc.to_dict().get('userUID')
        return None
    
    def get_notifications_enabled(self, uid: str):
        """Retrieves a user's notification preferences."""
        try:
            user_doc = self.db.collection('users').document(uid).get()
            if user_doc.exists:
                return user_doc.to_dict().get('notification_enabled', True)
            return True  # Default value if document doesn't exist
        except Exception as e:
            print(f"Error getting notification settings: {e}")
            return True
    
    def get_profile_picture(self, uid: str):
        """
        Retrieves a user's profile picture URL.

        Args:
            uid: Unique user identifier

        Returns:
            Profile picture URL (str) if found, empty string otherwise
        """
        try:
            user_doc = self.db.collection('users').document(uid).get()
            if user_doc.exists:
                return user_doc.to_dict().get('profilePic', '')
            return ''  # Default empty string if document doesn't exist
        except Exception as e:
            print(f"Error getting profile picture: {e}")
            return ''  # Default to empty string on error
    
    def get_user_by_uid(self, user_UID: str) -> Optional[User]: # TODO: Fix this
        """Retrieves a user by their ID.
        
        Args:
            user_UID: Unique user identifier
            
        Returns:
            User object if found, None otherwise
        """
        # Get username from user document
        username = self.get_username_by_uid(user_UID)

        # Get email from usernames document
        email = self.get_email_by_username(username) if username else None

        # Get user settings
        settings = Settings(user_UID,
                            self.get_notifications_enabled(user_UID),
                            self.get_profile_picture(user_UID))
        
        # Get user activities
        # activities = self.db_controller.get_activities(username) # TODO: Method might not be correctly implemented

        # Get user saved routes
        # saved_routes = self.db_controller.get_saved_routes(username) # TODO: Method might not be correctly implemented
        
        # Generated?    
        # # Get user filters
        # filters = Filters()
        # filters_data = data.get('filters', {})
        # filters._show_water_point = filters_data.get('show_water_point', False)
        # filters._show_repair_shop = filters_data.get('show_repair_shop', False)
        # user.filters = filters
            
        return User(uid=user_UID,
                    email=email,
                    username=username,
                    settings=settings,
                    # activities, #TODO: To be implemented
                    # saved_routes
                    )
    
    def user_exists(self, uid: str) -> bool:
        """Checks if a user exists in the database.
        
        Args:
            uid: Unique user identifier
            
        Returns:
            True if user exists, False otherwise
        """
        user_doc = self.db.collection('users').document(uid).get()
        return user_doc.exists

    def username_exists(self, username: str) -> bool:
        """Checks if a username is already taken.
        
        Args:
            username: Username to check
            
        Returns:
            True if username exists
        """
        user_doc = self.db.collection('usernames').document(username).get()
        return user_doc.exists
    
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
            self.db.collection('usernames').document(user.get_username()).set({
                'email': user.get_email(),
                'userUID': user.get_uid()
            })

            user_data = {
                'email': user.get_email(),
                'username': user.get_username(),
                'firstName': user.get_first_name(),
                'lastName': user.get_last_name(),
                'profilePic': user.get_settings().get_profile_picture() if user.get_settings() else '',
                'notification_enabled': user.get_settings().get_notification_enabled() if user.get_settings() else True,
                'created_at': firestore.SERVER_TIMESTAMP,
            }
            print(f"user_data: {user_data}")
            self.db.collection('users').document(user.get_uid()).set(user_data)
            self.db.collection('users').document(user.get_uid()).collection('savedRoutes').document("placeholder").set({"placeholder": True})
            self.db.collection('users').document(user.get_uid()).collection('activities').document("placeholder").set({"placeholder": True})
            
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
    
    def update_user_profile_picture(self, user_UID: str, profile_picture_url: str) -> bool:
        """Updates a user's profile picture.
        
        Args:
            user_UID: User identifier
            profile_picture: Binary image data
            
        Returns:
            True if successful
        """
        try:
            self.db.collection("users").document(user_UID).update({
                "profilePic": profile_picture_url
            })
            return {"message": "Profile picture updated", "url": profile_picture_url}, 200
        except Exception as e:
            print("Firestore update failed:", e)
            return {"message": "Failed to update Firestore"}, 500

    def update_user_email(self, user_UID, new_email):
        self.db.collection("users").document(user_UID).update({"email": new_email})
        users_ref = self.db.collection("usernames").where("userUID", "==", user_UID).stream()
        for doc_snapshot in users_ref:
            self.db.collection("usernames").document(doc_snapshot.id).update({"email": new_email})

    def update_username(self, user_UID, new_username):
        user_doc = self.db.collection("users").document(user_UID).get()
        if user_doc.exists:
            old_username = user_doc.to_dict().get("username")
            self.db.collection("usernames").document(old_username).delete()
            self.db.collection("usernames").document(new_username).set({
                "email": user_doc.to_dict().get("email"),
                "userUID": user_UID
            })
            self.db.collection("users").document(user_UID).update({"username": new_username})
            return jsonify({"message": "Username updated"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    # Activity methods
    def save_activity(self, activity: Activity) -> bool:
        
        # Prepare data for activity document
        doc_data = {
            "activityName": activity.get_activity_name(),
            "notes": activity.get_notes(),
            "distance": activity.get_route().get_distance(),
            "startPostal": activity.get_route().get_start_postal(),
            "endPostal": activity.get_route().get_end_postal(),
            "duration": activity.get_duration(),
            "routePath": activity.get_route().get_route_path(),
            "startTime": activity.get_start_time(),
            "instructions": activity.get_route().get_instructions(),
            "startLocation": activity.get_route().get_start_location(),
            "endLocation": activity.get_route().get_end_location(),
            "createdAt": activity.get_created_at()
        }

        self.db.collection("users").document(activity.get_user_uid()).collection("activities").add(doc_data)
        
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