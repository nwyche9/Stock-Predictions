import tensorflow as tf
from tensorflow.python.tools import freeze_graph, optimize_for_inference_lib

# freezing the graph with all the current values
freeze_graph.freeze_graph(input_graph='stock_prediction.pbtxt', input_saver='', input_binary=True,
                          input_checkpoint='stock_prediction.ckpt', output_node_names='y_output',
                          restore_op_name='save/restore all', filename_tensor_name='save/Const:0',
                          output_graph='frozen_stock_prediction.pb',
                          clear_devices=True, initializer_nodes='')


# getting it ready to transport to android app and loading it as a string
input_graph_def = tf.GraphDef()

# making it into a string file
with tf.gfile.Open('frozen_stock_prediction.pb', 'rb') as f:
    data = f.read()
    input_graph_def.ParseFromString(data)

# optimizing said graph
output_graph_def = optimize_for_inference_lib.optimize_for_inference(input_graph_def, ['x_input'], ['y_output'],
                                                                     tf.float32.as_datatype_enum)

# making a reference to the input graph def and writing it as a string
f = tf.gfile.FastGFile(name='optimized_stock_prediction.pb', mode='w')
f.write(file_content=output_graph_def.SerializeToString())
