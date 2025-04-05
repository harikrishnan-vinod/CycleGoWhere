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

def to_serializable(doc_dict):
    for key, value in doc_dict.items():
        if isinstance(value, firestore.GeoPoint):
            doc_dict[key] = {
                "latitude": value.latitude,
                "longitude": value.longitude
            }
        elif isinstance(value, dict):
            to_serializable(value)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], firestore.GeoPoint):
                    value[i] = {
                        "latitude": value[i].latitude,
                        "longitude": value[i].longitude
                    }
                elif isinstance(value[i], dict):
                    to_serializable(value[i])
    return doc_dict

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
        
    def get_user_activities(self, user_UID: str) -> List[Activity]:
        act_ref = self.db.collection("users").document(user_UID).collection("activities").stream()
        activities = []
        for doc in act_ref:
            data = doc.to_dict()
            route = self.get_route(user_UID, doc.id)
            activity = Activity(user_uid=user_UID,
                                activity_id=doc.id,
                                activity_name=data.get("activityName"),
                                notes=data.get("notes"),
                                duration=data.get("duration"),
                                start_time=data.get("startTime"),
                                route=route,
                                created_at=data.get("createdAt"))
            activities.append(activity)

        return activities
    
    def delete_activity(self, user_uid: str, activity_id: str) -> bool:
        """Deletes an activity from the database.
        
        Args:
            user_id: User identifier
            activity_id: Activity identifier
            
        Returns:
            True if successful
        """
        try:
            # Check if activity belongs to user
            activity_ref = self.db.collection("users").document(user_uid).collection('activities').document(activity_id)
            activity_doc = activity_ref.get()
            
            if not activity_doc.exists:
                return False
            
            if activity_doc.to_dict().get('user_id') != user_id:
                return False
            
            # Delete activity
            activity_ref.delete()
            
            return True
        except Exception as e:
            print(f"Error deleting activity: {e}")
            return False
    
    # Route methods
    def get_route(self, user_UID: str, activity_ID) -> Optional[Route]:
        doc = self.db.collection("users").document(user_UID).collection("activities").document(activity_ID).get()
        if doc.exists:
            data = doc.to_dict()
            route = Route(start_location=data.get("startLocation"),
                          start_postal=data.get("startPostal"),
                          end_location=data.get("endLocation"),
                          end_postal=data.get("endPostal"),
                          distance=data.get("distance"),
                          route_path=data.get("routePath"),
                          instructions=data.get("instructions"))
            return route
        return None
    
    # SavedRoutes methods
    def get_saved_routes(self, user_uid: str) -> List[Route]:
        route_ref = self.db.collection("users").document(user_uid).collection("savedRoutes").stream()
        routes = []
        for doc in route_ref:
            data = doc.to_dict()
            route = Route(route_name=data.get("routeName"),
                          notes=data.get("notes"),
                          distance=data.get("distance"),
                          start_postal=data.get("startPostal"),
                          end_postal=data.get("endPostal"),
                          route_path=data.get("routePath"),
                          instructions=data.get("instructions"),
                          start_location=data.get("startLocation"),
                          end_location=data.get("endLocation"),
                          last_used_at=data.get("lastUsedAt"),
                          route_id=doc.id)
            routes.append(route)

        return routes
    
    def save_route(self, user_uid: str, route: Route) -> bool:
        # Prepare data for route document
        doc_data = {
                "routeName": route.get_route_name(),
                "notes": route.get_notes(),
                "distance": route.get_distance(),
                "startPostal": route.get_start_postal(),
                "endPostal": route.get_end_postal(),
                "routePath": route.get_route_path(),
                "instructions": route.get_instructions(),
                "startLocation": route.get_start_location(),
                "endLocation": route.get_end_location(),
                "lastUsedAt": route.get_last_used_at()
            }
        
    def update_last_used(self, user_uid: str, route_id: str) -> bool:
        route_ref = self.db.collection("users").document(user_uid).collection("savedRoutes").document(route_id)
        if route_ref.get().exists:
            route_ref.update({"lastUsedAt": firestore.SERVER_TIMESTAMP})
            return True
        return False
 
    def unsave_route(self, user_uid: str, route_id: str) -> bool:
        """Removes a saved route for a user.
        
        Args:
            user_id: User identifier
            route_id: Route identifier
            
        Returns:
            True if successful
        """
        try:
            # Delete saved route entry
            self.db.collection("users").document(user_uid).collection("savedRoutes").document(route_id).delete()
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