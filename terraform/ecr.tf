resource "aws_ecr_repository" "discord_toybox" {
  name                 = "discord_toybox"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "discord_toybox"
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.discord_toybox.repository_url
}
