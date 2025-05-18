class TransformResult:
	def __init__(self, success, free=False):
		self.success = success

		# A 'free' transform is one that doesn't count toward the limit of transforms to apply
		self.free = free
