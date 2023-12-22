resource "aws_lb" "discord_toybox_alb" {
  name               = "discord-toybox-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.discord_toybox_sg.id]
  subnets            = [aws_subnet.discord_toybox_1.id, aws_subnet.discord_toybox_2.id]

  enable_deletion_protection = false

  tags = {
    Name = "discord-toybox-alb"
  }
}

resource "aws_lb_target_group" "discord_toybox_tg" {
  name     = "discord-toybox-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.discord_toybox.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    path                = "/"
    protocol            = "HTTP"
    interval            = 30
    matcher             = "200-299"
  }

  tags = {
    Name = "discord-toybox-tg"
  }
}

resource "aws_lb_listener" "discord_toybox_listener" {
  load_balancer_arn = aws_lb.discord_toybox_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.discord_toybox_tg.arn
  }
}