output "cluster_name" {
  description = "The name of the EKS cluster"
  value       = aws_eks_cluster.example.name
}

output "node_group_name" {
  description = "The name of the EKS node group"
  value       = aws_eks_node_group.example.node_group_name
}

output "region" {
  description = "The AWS region where the cluster is deployed"
  value       = var.region
}
