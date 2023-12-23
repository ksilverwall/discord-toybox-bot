resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 1
  min_capacity       = 0
  resource_id        = "service/${aws_ecs_cluster.discord_toybox_bot.name}/${aws_ecs_service.discord_toybox_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_scheduled_action" "scale_up" {
  name               = "scale-up-at-9pm-jst"
  service_namespace  = "ecs"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  schedule           = "cron(0 12 * * ? *)" # JST 21:00
  scalable_target_action {
    min_capacity = 1
    max_capacity = 1
  }
}

resource "aws_appautoscaling_scheduled_action" "scale_down" {
  name               = "scale-down-at-midnight-jst"
  service_namespace  = "ecs"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  schedule           = "cron(0 15 * * ? *)" # JST 24:00
  scalable_target_action {
    min_capacity = 0
    max_capacity = 0
  }
}
