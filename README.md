# BISINDO App

This repository hosts the BISINDO app. BISINDO (Bahasa Isyarat Indonesia) aims to enhance communication through sign language recognition and translation. The app provides real-time interpretations to facilitate inclusivity for the deaf and hard-of-hearing communities.

## Features
- **Sign Language Recognition**: Utilize AI/ML models to identify and translate BISINDO gestures.
- **Customizable Settings**: Tailor the experience using `settings.json`.
- **Modular Components**: Code organized into reusable `components`.
- **Multimedia Assets**: Static images or other resources in `assets`.
- **User-Friendly Pages**: Manage app navigation via `pages`.

## Project Structure
The repository is organized as follows:  
- **`assets/`**: Static resources such as icons or images used by the app.  
- **`components/`**: Reusable UI and app components.  
- **`core/`**: Core application logic and utilities.  
- **`installer/`**: Installation scripts and related files.  
- **`pages/`**: Definitions for different app views or screens.  
- **`.gitignore`**: Git configuration to skip unnecessary files in version control.  
- **`BisindoApp.spec`**: Configuration or packaging instructions for the app.
- **`label_dict.json`**: JSON file for machine learning label mappings.
- **`main.py`**: Entry point for running the application.
- **`model.p`**: Pre-trained machine learning model, serialized for usage.
- **`requirements.txt`**: Python project dependencies.  
- **`settings.json`**: Configurable application settings.

## Getting Started
### Prerequisites
- Python 3.8 or above  

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/Ayash13/BISINDO-App-Flet-Side.git
   ```
2. Navigate to the project directory:  
   ```bash
   cd BISINDO-App-Flet-Side
   ```
3. Install the dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To launch the app, run:
```bash
python main.py
```

## Licensing
This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.

## Contribution
Feel free to fork the repository, report issues, or submit pull requests.

## Acknowledgements
This app and its development were motivated by the needs of the diverse BISINDO community.  Special thanks to researchers and contributors in the field of sign language recognition.