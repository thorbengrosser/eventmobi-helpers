# EventMobi Dummy Data Generator

## Overview
This tool is designed to generate dummy data for EventMobi events. It's intended for development and testing purposes only and should not be used on live events. The tool generates fictitious yet plausible data for people, sessions, and companies associated with an event, helping developers and testers simulate real-world usage scenarios.

## Features
- **Generate People**: Simulates event participants, with a configurable number of attendees and speakers.
- **Generate Sessions**: Creates sessions with randomly assigned speakers and valid time slots.
- **Generate Companies**: Adds companies with basic contact information and descriptions.

## Warning
**DO NOT USE THIS TOOL ON A LIVE EVENT.** This is not an official EventMobi add-on. Use this tool only in a development or testing environment.

## Prerequisites
Before you can use this tool, you'll need:
- Python 3.x
- Required Python libraries: `requests`, `faker`, `pytz`
- An API key and Event ID from your EventMobi account

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/eventmobi-dummy-data-generator.git
cd eventmobi-dummy-data-generator
```

Install the necessary Python packages:
```bash
pip install requests faker pytz
```

## Usage

Run the script from the command line:
```bash
python dummy_data_generator.py
```

Follow the on-screen prompts to enter your Event ID, API key, and the number of entities (people, sessions, companies) you wish to generate.

## How It Works

- **Step 1**: Enter your Event ID and API key.
- **Step 2**: Specify the number of people, sessions, and companies you want to generate.
- **Step 3**: The script interacts with the EventMobi API to create data.
- **Step 4**: Data is uploaded in batches, and progress is displayed via a console spinner.

## Contributing

Contributions are welcome! If you have improvements or bug fixes, please fork the repository and submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
