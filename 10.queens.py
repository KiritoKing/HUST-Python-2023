class Queens:
	def solveNQueens(self, n):
		self.helper([-1]*n, 0, n)

	def helper(self, columnPosition, rowindex, n):#ding
		# print(rowindex)
		if rowindex == n:
			self.printSolution(columnPosition, n)
			# print(columnPosition)
			return 
		# for column in range(n-rowindex):
		for column in range(n):
			columnPosition[rowindex] = column
			if self.isValid(columnPosition, rowindex):
				self.helper(columnPosition, rowindex+1, n)

	def isValid(self, columnPosition, rowindex):
		if len(set(columnPosition[ :rowindex+1]))!=len(columnPosition[:rowindex+1]):
			# print(columnPosition, rowindex)
			return False
		for i in range(rowindex):
			if abs(columnPosition[i]-columnPosition[rowindex]) == int(rowindex-i):
				# print(columnPosition, rowindex)
				return False
		return True
	def printSolution(self, columnPosition, n):
		# print(columnPosition)
		for row in range(n):
			line = ""
			for column in range(n):
				if columnPosition[row] == column:
					line += "Q\t"
				else:
					line += ".\t"
			print(line, "\n")
		print('\n')

if __name__ == '__main__':
  Queens().solveNQueens(8)