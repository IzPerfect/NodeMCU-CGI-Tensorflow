#!C:\Python35\python.exe

import tensorflow as tf
import numpy as np
import time

tf.set_random_seed(180508)
learning_rate = 0.01


X = tf.placeholder(tf.float32, [None, 2])
Y = tf.placeholder(tf.float32, [None, 1])

W1 = tf.Variable(tf.random_normal([2, 10]), name='weight1')
b1 = tf.Variable(tf.random_normal([10]), name='bias1')
l1 = tf.sigmoid(tf.matmul(X, W1) + b1)

W2 = tf.Variable(tf.random_normal([10, 20]), name='weight2')
b2 = tf.Variable(tf.random_normal([20]), name='bias2')
l2 = tf.sigmoid(tf.matmul(l1, W2) + b2)

W3 = tf.Variable(tf.random_normal([20, 1]), name='weight3')
b3 = tf.Variable(tf.random_normal([1]), name='bias3')

hypothesis = tf.sigmoid(tf.matmul(l2, W3) + b3)

# cost
cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) *
                       tf.log(1 - hypothesis))
# minimize the cost
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Accuracy, hypothesis is true if hypothesis > 0.5
predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

# resue to use restore
saver = tf.train.Saver()
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

save_path = "./xor_weights/xor_weights.ckpt-1000"
saver.restore(sess, save_path)



def prediction(input1, input2):
    result = sess.run(predicted, feed_dict={X: np.array([input1, input2]).reshape([-1,2])})
    return result
