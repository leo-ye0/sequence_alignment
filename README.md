basic3.py is a basic dynamic programming approach.  
efficient3.py is a memory efficient approach which combines divide and conquer and dynamic programming.  
# Summary
The basic algorithm increases memory usage polynomially with input size because it builds a full dynamic programming (DP) table of size 𝑚×𝑛, leading to O(mn) space complexity and memory usage   that can reach tens or hundreds of megabytes for large inputs. In contrast, the efficient algorithm applies a divide-and-conquer approach that only computes and stores partial score rows   during recursion, reducing its space complexity to O(n). As a result, its memory usage grows much more slowly and typically remains within a few megabytes, even as the input size scales   significantly.  
The CPU time for both basic and efficient algorithms shows a polynomial increasing as the problem size increases. They both takes O(mn) time complexity, but the efficient algorithm based on divide and conquer does not reduce its time complexity due to more recursive calls. So, more calculations result in higher CPU time for efficient algorithm, making it slower than the basic algorithm when dealing with large inputs.






