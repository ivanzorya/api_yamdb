# api_yamdb
### REST API for a service — a database of reviews on movies, books, and music.

The YaMDb project collects user reviews (Review) on various works (Title). Works are divided into categories: "Books", "Movies", "Music". The list of categories (Category) can be expanded (for example, by adding a category like "Visual Arts" or "Jewelry").
The works themselves are not stored in YaMDb; you cannot watch a movie or listen to music here.
Each category contains works: books, movies, or music. For example, in the "Books" category, there might be works like "Winnie-the-Pooh and All, All, All" and "The Martian Chronicles", while in the "Music" category, there might be the song "Recently" by the band "Insects" and Bach's Second Suite. A work can be assigned a genre from a predefined list (for example, "Fairy Tale", "Rock", or "Art House"). New genres can only be created by an administrator.
Grateful or outraged readers leave textual reviews (Review) on works and rate the work (a score ranging from one to ten). The average rating of the work is automatically calculated from numerous scores.

### User Roles
-   Anonymous — can view descriptions of works, read reviews and comments.
-   Authenticated user (user) — can read everything like an Anonymous user, additionally can publish reviews and rate works (movies/books/songs), can comment on other users' reviews and rate them; can edit and delete their own reviews and comments.
-   Moderator (moderator) — has the same rights as an Authenticated user plus the right to delete and edit any reviews and comments.
-   Administrator (admin) — has full rights to manage the project and all its content. Can create and delete works, categories, and genres. Can assign roles to users.
-   Django Administrator — has the same rights as the Administrator role.

### User Registration Algorithm
-   The user sends a POST request with the email parameter to /api/v1/auth/email/.
-   YaMDB sends an email with a confirmation code to the provided email address.
-   The user sends a POST request with the email and confirmation code parameters to /api/v1/auth/token/, and in response, they receive a token (JWT token).
-   These operations are performed once during user registration. As a result, the user receives a token and can work with the API, sending this token with each request.
-   After registration and receiving the token, the user can send a PATCH request to /api/v1/users/me/ and fill in the fields in their profile (field descriptions are in the documentation).

### YaMDb API Resources
-   AUTH Resource: authentication.
-   USERS Resource: users.
-   TITLES Resource: works to which reviews are written (a specific movie, book, or song).
-   CATEGORIES Resource: categories (types) of works ("Movies", "Books", "Music").
-   GENRES Resource: genres of works. A single work can be linked to several genres.
-   REVIEWS Resource: reviews on works. A review is linked to a specific work.
-   COMMENTS Resource: comments on reviews. A comment is linked to a specific review.

### Each resource is described in the documentation: endpoints (addresses to which requests can be made), allowed request types, access rights, and additional parameters if necessary.

### Related Data and Cascading Deletion
-   When a User object is deleted, all reviews and comments by this user (along with ratings) are deleted.
-   When a Title object is deleted, all reviews and comments related to this work are deleted.
-   When a Category object is deleted, works associated with this category (Title) are not deleted.
-   When a Genre object is deleted, works associated with this genre (Title) are not deleted.
-   When a Review object is deleted, all comments related to this review are deleted.
