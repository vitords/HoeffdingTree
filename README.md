# HoeffdingTree
A Python implementation of the Hoeffding Tree algorithm, also known as Very Fast Decision Tree (VFDT).

The Hoeffding Tree is a decision tree for classification tasks in data streams.

```
Pedro Domingos and Geoff Hulten. 2000. Mining high-speed data streams. 
In Proceedings of the sixth ACM SIGKDD international conference on
  Knowledge discovery and data mining (KDD '00). 
ACM, New York, NY, USA, 71-80.
```

This implementation was initially based on [Weka](http://www.cs.waikato.ac.nz/ml/weka/)'s Hoeffding Tree and the original work by Geoff Hulten and Pedro Domingos, [VFML](http://www.cs.washington.edu/dm/vfml/). Although it is based on these I cannot guarantee that the algorithm will work exactly, or even produce the same output, as any of these implementations. Most of the class and variable names, for example, follow Weka's implementation in order to ease the use of the algorithm for some of my peers who are used to Weka when performing data mining tasks, but there may be significant changes in the code behind it.
