# Intro to Socket Programming with Python

## Description

This repo serves as personal documentation for labs encountered in a networking analysis class. The labs come from the book, _Computer Networking: A Top-Down Approach_ by **James F. Kurose & Keith W. Ross**, but the solutions to them are very much my own.

This is a work in progress and this README will be updated accordingly.

## Implemented Labs

- [Usage](#usage)
- [Web Server](./1-WebServerLab/README.md)
- [UDP Pinger](./2-UDP-PingerLab/README.md)

## Usage

Clone the repo

```bash
git clone https://github.com/iiTONELOC/socket-programming-w-python.git
```

The labs can be run locally by navigating to the directory for the lab you wish to see. You would first navigate to the README contained in that lab's directory. The README provides the information for each lab as given by Kurose & Ross, (2023), a proposed solution written by me, example output, and usage instructions.

For example, to see the Web Server Lab:

```bash
#navigate to the folder
cd 1-WebServerLab/

# view the readme
## via cli
cat README.md

## via code editor
code README.md
```

Examining the README we can see that this project can be run using the server.py or server-opt1.py

```bash

#run proposed solution
python server.py

#run the option 1
python server-opt1.py

```

## References

Kurose, J., & Ross, K. (2022). Computer networking: A top-down approach (8th ed.). Pearson Higher Ed.

Kurose, J., & Ross, K. (2023). Programming Assignments. Computer Network Research Group - UMass Amherst.
Retrieved September 8, 2023, from https://gaia.cs.umass.edu/kurose_ross/programming.php

## LICENSE

This project is licensed with the MIT License, [a copy can be found here](./LICENSE).
