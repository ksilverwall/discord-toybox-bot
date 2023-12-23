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

#
# Internet Gateway
#
resource "aws_internet_gateway" "discord_toybox_igw" {
  vpc_id = aws_vpc.discord_toybox.id
  tags = {
    Name = "discord-toybox-igw"
  }
}

#
# Route Table
#
resource "aws_route_table" "discord_toybox_rt" {
  vpc_id = aws_vpc.discord_toybox.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.discord_toybox_igw.id
  }

  tags = {
    Name = "discord-toybox-rt"
  }
}

resource "aws_route_table_association" "discord_toybox_rta_1" {
  subnet_id      = aws_subnet.discord_toybox_1.id
  route_table_id = aws_route_table.discord_toybox_rt.id
}

resource "aws_route_table_association" "discord_toybox_rta_2" {
  subnet_id      = aws_subnet.discord_toybox_2.id
  route_table_id = aws_route_table.discord_toybox_rt.id
}
