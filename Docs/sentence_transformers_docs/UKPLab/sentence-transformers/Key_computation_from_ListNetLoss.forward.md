logits_matrix = torch.full((batch_size, max_docs), -1e16, device=self.model.device)
labels_matrix = torch.full_like(logits_matrix, float("-inf"))