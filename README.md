# Online Learning Platform

This is an online learning platform built using Python Flask. It leverages gRPC for communication, OPA (Open Policy Agent) for authorization, and Keycloak for authentication.

## Features

- **Python Flask**: A micro web framework for building the platform.
- **gRPC**: Used for efficient communication between services.
- **OPA (Open Policy Agent)**: Provides fine-grained authorization.
- **Keycloak**: Manages authentication and user management.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/QusaiKhalid/online-learning-platform.git
   cd online-learning-platform
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure Keycloak and OPA as per the documentation.

## Usage

1. Start the Flask server:

   ```bash
   flask run
   ```

2. Access the platform at `http://localhost:5000`.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries, please contact [quamnsour@gmail.com].
