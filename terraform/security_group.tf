resource "aws_security_group" "discord_toybox_sg" {
  name        = "discord-toybox-sg"
  description = "Allow HTTP"
  vpc_id      = aws_vpc.discord_toybox.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "discord-toybox-sg"
  }
}
