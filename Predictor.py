import tensorflow as tf
from Data_Handler import build_subsets



# accuracy function expected is the y_input actual are the actual outputs
# checking the arrays to see if the first(maximum) values are the same(equal)
def accuracy(actual, expected):
    num_correct = 0
    for i in range(len(actual)):
        actual_value= actual[i]
        expected_value = expected[i]
        if actual_value[0] >= actual_value[1] and expected_value[0] >= expected_value[1]:
            num_correct += 1
        elif actual_value[0] <= actual_value[1] and expected_value[0] <= expected_value[1]:
            num_correct +=1
    return (num_correct/len(actual)) * 100

# need to limit how far back the data goes and how much data comes in
x_train, y_train = build_subsets('RIOT', '20180101', '20180927')

x_test, y_test = build_subsets('RIOT', '20180927', '20181006')


# made the base model here
x_input = tf.placeholder(dtype=tf.float32, shape=[None, 5], name='x_input')
y_input = tf.placeholder(dtype=tf.float32, shape=[None, 2], name='y_input')

W = tf.Variable(initial_value=tf.ones(shape=[5, 2]))
b = tf.Variable(initial_value=tf.ones(shape=[2]))

y_output = tf.add(tf.matmul(x_input, W), b, name='y_output')

# making the loss function
# the tf.nn thing takes in the correct output with the actual output to reduce the loss
loss = tf.reduce_sum(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_input, logits=y_output)))
# different type of optimizer
optimizer = tf.train.AdamOptimizer(0.01).minimize(loss)


saver = tf.train.Saver()

# initializing the session
session = tf.Session()
session.run(tf.global_variables_initializer())

tf.train.write_graph(session.graph_def, '.', 'stock_prediction.pbtxt', False)

for _ in range(20000):
    session.run(optimizer, feed_dict={x_input: x_train, y_input: y_train})

saver.save(session, save_path='./stock_prediction.ckpt')

print(accuracy(session.run(y_output, feed_dict={x_input: x_train}), y_train))
print(accuracy(session.run(y_output, feed_dict={x_input: x_test}), y_test))


