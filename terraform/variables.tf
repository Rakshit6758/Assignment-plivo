variable "region" {
  description = "The AWS region to deploy the cluster"
  default     = "ap-south-1"
}

variable "cluster_name" {
  description = "The name of the EKS cluster"
  default     = "example-cluster"
}

variable "node_group_name" {
  description = "The name of the EKS node group"
  default     = "example-node-group"
}

variable "desired_size" {
  description = "The desired number of worker nodes"
  default     = 2
}

variable "max_size" {
  description = "The maximum number of worker nodes"
  default     = 3
}

variable "min_size" {
  description = "The minimum number of worker nodes"
  default     = 1
}
