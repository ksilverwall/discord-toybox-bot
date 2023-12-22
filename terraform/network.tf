resource "aws_vpc" "discord_toybox" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "discord-toybox-vpc"
  }
}

resource "aws_subnet" "discord_toybox_1" {
  vpc_id     = aws_vpc.discord_toybox.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-northeast-1a"
  tags = {
    Name = "discord-toybox-subnet-1"
  }
}

resource "aws_subnet" "discord_toybox_2" {
  vpc_id     = aws_vpc.discord_toybox.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ap-northeast-1c"
  tags = {
    Name = "discord-toybox-subnet-2"
  }
}

resource "aws_internet_gateway" "discord_toybox_igw" {
  vpc_id = aws_vpc.discord_toybox.id
  tags = {
    Name = "discord-toybox-igw"
  }
}
