# The AWS Cloud Conjurer
## Getting the Machine Part
Welcome magicians! If you came from playing the (game)[https://elainechan01.itch.io/the-aws-cloud-conjurer], please read the following instructions _in sequence_.

### Part 1
This is for the **host**! Feel free to share your screen for this part so the team can all learn together.
1. Launch an EC2 instance 
    1. Use the following specs:
        - AMI: Amazon Linux 2023 AMI
        - Architecture: 64-bit (Arm)
        - Instance Type: t4g.nano
    2. Create a Key-Pair _**do not share your downloaded key-pair file + store this somewhere safe!**_
    3. Add the following security group rules (Network Settings > Edit > Security Group Rules):
        1. SSH access for management
            - Type: SSH
            - Source Type: Anywhere
        2. Inbound traffic on port 8765
            - Type: Custom TCP
            - Port: 8765
            - Source Type: Anywhere
2. Connect to your EC2 instance using EC2 Instance Connect
3. Run the following commands.
    ```
    sudo yum update -y
    sudo yum install -y python3-pip
    sudo yum install git -y
    git clone https://github.com/elainechan01/the-aws-cloud-conjurer.git magic
    cd magic
    ./dist/server
    ```
    Your server should've started! Stop your screen share here.

### Part 2
This is for everyone. The goal is to connect to the server *one-by-one* and a clue should form. This task will require 5 connections in total - if your team does not have that many members, someone will have to rerun the following steps in a new terminal.

The process will require players to have the following installed:
- python
- pip
1. Launch the terminal on your local machine and run the following. Feel free to use a `venv` if you prefer.
    ```
    git clone https://github.com/elainechan01/the-aws-cloud-conjurer.git magic
    cd magic
    pip install pygame
    pip install websockets
    python3 source/game.py
    ```
2. You should see a prompt to Enter the EC2 instance IP address. The host will need to provide this for you (refer to Public IPv4 address on your Instance Management Console). Remember to connect *one-by-one* - once you've entered the address and hit `Enter` on your keyboard, you will be connected to the server and you should see a PyGame window.
3. For each connection, take note of your letter e.g., connection 1 = 'A', connection 2 = 'B'. With all the letters, what word can you form? That's the name of the machine part needed.

### Finally
This is for the **host**!
1. On your EC2 instance connection, press `Ctrl+C` to stop the server.
2. Back on your Instance Management Console, select your instance and under Instance State, select Stop Instance.
3. Finally, terminate your instance to avoid additional charges.
