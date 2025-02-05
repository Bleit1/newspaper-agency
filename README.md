Newspaper Agency

A Django-based web application that simulates a newspaper agency. New users are immediately prompted to register when visiting the site, and they can then view, comment on, and react to news articles. Only users with specific permissions (e.g., assigned via the admin panel) are allowed to create news.
Features

    User Registration & Authentication
        Registration: The site opens with a registration page by default.
        Login/Logout: Custom login and logout views are provided.
        Permissions: By default, new users can only read news, comment, and react. Only users with the appropriate permissions (e.g., via a “News Editors” group) can create news.

    News Display & Filtering
        Main News: Displays featured news with pagination.
        Latest News: Uses a “Load More” button to display additional news items.
        Filtering & Search: Users can search news by title and filter by topics (genres).

    Comments and Reactions
        Authenticated users can post comments on news articles.
        Users can add reactions (like/dislike) to articles.

    Responsive Design
        Uses Bootstrap 4 and custom CSS for a modern, responsive UI.
        A navigation menu with links for Main, Latest, Create News (if permitted), Register, Login, and Logout.