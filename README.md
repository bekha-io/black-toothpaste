# Blog API

This is a Django-powered RESTful API for managing blog posts and polls.

Documentation is available here: https://documenter.getpostman.com/view/22853773/2s9XxsUbKY

## Endpoints

### Posts

- **List all posts and create a new one**

  - `GET /api/posts`

    Get a list of all blog posts.

  - `POST /api/posts`

    Create a new blog post.

- **Get post by ID**

  - `GET /api/posts/<int:pk>`

    Get a specific blog post by its ID.

- **Update a post**

  - `PUT /api/posts/<int:pk>/update`

    Update a specific blog post by its ID.

### Polls

- **List all polls and create a new one**

  - `GET /api/polls`

    Get a list of all polls.

  - `POST /api/polls`

    Create a new poll.

- **Get poll by ID**

  - `GET /api/polls/<int:pk>`

    Get a specific poll by its ID.

### Poll Answers

- **Submit a user's poll answer**

  - `POST /api/polls/answer`

    Submit a user's answer to a poll. The request should include the user's ID, poll ID, and the selected answer choice.

---

Replace the `<int:pk>` placeholder with the corresponding numeric ID for each resource. Also, provide a brief description of each endpoint and the necessary request parameters and data.

Feel free to expand on this template and add additional details about your project, such as how to run the development server, database setup, or any other relevant information.

Make sure to include the project structure, how to install dependencies, and any other instructions necessary for someone to successfully use and contribute to your project.