# Keras imports
import warnings

from keras import backend as K
from keras.engine.topology import get_source_inputs
from keras.applications.imagenet_utils import _obtain_input_shape
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Flatten, Dense, Input, Dropout, Activation
from keras.models import Model
from keras.regularizers import l2
from keras.utils.data_utils import get_file
from keras.utils.layer_utils import convert_all_kernels_in_model

TH_WEIGHTS_PATH = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/' \
                  'vgg16_weights_th_dim_ordering_th_kernels.h5'
TF_WEIGHTS_PATH = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/' \
                  'vgg16_weights_tf_dim_ordering_tf_kernels.h5'
TH_WEIGHTS_PATH_NO_TOP = 'https://github.com/fchollet/deep-learning-models/releases/download/' \
                         'v0.1/vgg16_weights_th_dim_ordering_th_kernels_notop.h5'
TF_WEIGHTS_PATH_NO_TOP = 'https://github.com/fchollet/deep-learning-models/releases/download/' \
                         'v0.1/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'


def build_vgg(img_shape=(3, 224, 224), n_classes=1000, n_layers=16, weight_decay=5e-4,
              load_pretrained=False, freeze_layers_from='base_model'):
    # Decide if load pretrained weights from imagenet
    if load_pretrained:
        weights = 'imagenet'
    else:
        weights = None

    # Get base model
    if n_layers == 16:
        base_model = vgg16(include_top=False, weights=weights,
                           input_tensor=None, input_shape=img_shape,
                           weight_decay=weight_decay)
    elif n_layers == 19:
        base_model = vgg19(include_top=False, weights=weights,
                           input_tensor=None, input_shape=img_shape,
                           weight_decay=weight_decay)
    else:
        raise ValueError('Number of layers should be 16 or 19')

    # Add final layers
    x = base_model.output
    x = Flatten(name="flatten")(x)
    x = Dense(4096, activation='relu', W_regularizer=l2(weight_decay),
              b_regularizer=l2(weight_decay), name='dense_1')(x)
    x = Dropout(0.5)(x)
    x = Dense(4096, activation='relu', W_regularizer=l2(weight_decay),
              b_regularizer=l2(weight_decay), name='dense_2')(x)
    x = Dropout(0.5)(x)
    x = Dense(n_classes, W_regularizer=l2(weight_decay),
              b_regularizer=l2(weight_decay), name='dense{}'.format(n_classes))(x)
    predictions = Activation("softmax", name="softmax")(x)

    # This is the model we will train
    model = Model(input=base_model.input, output=predictions)

    # Freeze some layers
    if freeze_layers_from is not None:
        if freeze_layers_from == 'base_model':
            print ('   Freezing base model layers')
            for layer in base_model.layers:
                layer.trainable = False
        else:
            for i, layer in enumerate(model.layers):
                print(i, layer.name)
            print ('   Freezing from layer 0 to ' + str(freeze_layers_from))
            for layer in model.layers[:freeze_layers_from]:
                layer.trainable = False
            for layer in model.layers[freeze_layers_from:]:
                layer.trainable = True

    return model


def vgg16(include_top=True, weights='imagenet',
          input_tensor=None, input_shape=None,
          classes=1000, weight_decay=5e-4):
    """Instantiate the VGG16 architecture,
    optionally loading weights pre-trained
    on ImageNet. Note that when using TensorFlow,
    for best performance you should set
    `image_dim_ordering="tf"` in your Keras config
    at ~/.keras/keras.json.
    The model and the weights are compatible with both
    TensorFlow and Theano. The dimension ordering
    convention used by the model is the one
    specified in your Keras config file.
    # Arguments
        include_top: whether to include the 3 fully-connected
            layers at the top of the network.
        weights: one of `None` (random initialization)
            or "imagenet" (pre-training on ImageNet).
        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)
            to use as image input for the model.
        input_shape: optional shape tuple, only to be specified
            if `include_top` is False (otherwise the input shape
            has to be `(224, 224, 3)` (with `tf` dim ordering)
            or `(3, 224, 244)` (with `th` dim ordering).
            It should have exactly 3 inputs channels,
            and width and height should be no smaller than 48.
            E.g. `(200, 200, 3)` would be one valid value.
        classes: optional number of classes to classify images
            into, only to be specified if `include_top` is True, and
            if no `weights` argument is specified.
    # Returns
        A Keras model instance.
    """
    if weights not in {'imagenet', None}:
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization) or `imagenet` '
                         '(pre-training on ImageNet).')

    if weights == 'imagenet' and include_top and classes != 1000:
        raise ValueError('If using `weights` as imagenet with `include_top`'
                         ' as true, `classes` should be 1000')
    # Determine proper input shape
    input_shape = _obtain_input_shape(input_shape,
                                      default_size=224,
                                      min_size=48,
                                      dim_ordering=K.image_dim_ordering(),
                                      include_top=include_top)

    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor
    # Block 1
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block1_conv1')(img_input)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block2_conv1')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block3_conv1')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block3_conv2')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block4_conv1')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block4_conv2')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block5_conv1')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block5_conv2')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)

    if include_top:
        # Classification block
        x = Flatten(name='flatten')(x)
        x = Dense(4096, activation='relu', W_regularizer=l2(weight_decay),
                  b_regularizer=l2(weight_decay), name='fc1')(x)
        x = Dense(4096, activation='relu', W_regularizer=l2(weight_decay),
                  b_regularizer=l2(weight_decay), name='fc2')(x)
        x = Dense(classes, activation='softmax', W_regularizer=l2(weight_decay),
                  b_regularizer=l2(weight_decay), name='predictions')(x)

    # Ensure that the model takes into account
    # any potential predecessors of `input_tensor`.
    if input_tensor is not None:
        inputs = get_source_inputs(input_tensor)
    else:
        inputs = img_input
    # Create model.
    model = Model(inputs, x, name='vgg16')

    # load weights
    if weights == 'imagenet':
        if K.image_dim_ordering() == 'th':
            if include_top:
                weights_path = get_file('vgg16_weights_th_dim_ordering_th_kernels.h5',
                                        TH_WEIGHTS_PATH,
                                        cache_subdir='models')
            else:
                weights_path = get_file('vgg16_weights_th_dim_ordering_th_kernels_notop.h5',
                                        TH_WEIGHTS_PATH_NO_TOP,
                                        cache_subdir='models')
            model.load_weights(weights_path)
            if K.backend() == 'tensorflow':
                warnings.warn('You are using the TensorFlow backend, yet you '
                              'are using the Theano '
                              'image dimension ordering convention '
                              '(`image_dim_ordering="th"`). '
                              'For best performance, set '
                              '`image_dim_ordering="tf"` in '
                              'your Keras config '
                              'at ~/.keras/keras.json.')
                convert_all_kernels_in_model(model)
        else:
            if include_top:
                weights_path = get_file('vgg16_weights_tf_dim_ordering_tf_kernels.h5',
                                        TF_WEIGHTS_PATH,
                                        cache_subdir='models')
            else:
                weights_path = get_file('vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5',
                                        TF_WEIGHTS_PATH_NO_TOP,
                                        cache_subdir='models')
            model.load_weights(weights_path)
            if K.backend() == 'theano':
                convert_all_kernels_in_model(model)
    return model


def vgg19(include_top=True, weights='imagenet',
          input_tensor=None, input_shape=None,
          classes=1000, weight_decay=5e-4):
    """Instantiate the VGG19 architecture,
    optionally loading weights pre-trained
    on ImageNet. Note that when using TensorFlow,
    for best performance you should set
    `image_dim_ordering="tf"` in your Keras config
    at ~/.keras/keras.json.
    The model and the weights are compatible with both
    TensorFlow and Theano. The dimension ordering
    convention used by the model is the one
    specified in your Keras config file.
    # Arguments
        include_top: whether to include the 3 fully-connected
            layers at the top of the network.
        weights: one of `None` (random initialization)
            or "imagenet" (pre-training on ImageNet).
        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)
            to use as image input for the model.
        input_shape: optional shape tuple, only to be specified
            if `include_top` is False (otherwise the input shape
            has to be `(224, 224, 3)` (with `tf` dim ordering)
            or `(3, 224, 244)` (with `th` dim ordering).
            It should have exactly 3 inputs channels,
            and width and height should be no smaller than 48.
            E.g. `(200, 200, 3)` would be one valid value.
        classes: optional number of classes to classify images
            into, only to be specified if `include_top` is True, and
            if no `weights` argument is specified.
    # Returns
        A Keras model instance.
    """
    if weights not in {'imagenet', None}:
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization) or `imagenet` '
                         '(pre-training on ImageNet).')

    if weights == 'imagenet' and include_top and classes != 1000:
        raise ValueError('If using `weights` as imagenet with `include_top`'
                         ' as true, `classes` should be 1000')
    # Determine proper input shape
    input_shape = _obtain_input_shape(input_shape,
                                      default_size=224,
                                      min_size=48,
                                      dim_ordering=K.image_dim_ordering(),
                                      include_top=include_top)

    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor
    # Block 1
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block1_conv1')(img_input)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block2_conv1')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block3_conv1')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block3_conv2')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block3_conv3')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block3_conv4')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block4_conv1')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block4_conv2')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block4_conv3')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block4_conv4')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block5_conv1')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block5_conv2')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block5_conv3')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', W_regularizer=l2(weight_decay),
                      b_regularizer=l2(weight_decay), name='block5_conv4')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)

    if include_top:
        # Classification block
        x = Flatten(name='flatten')(x)
        x = Dense(4096, activation='relu', W_regularizer=l2(weight_decay),
                  b_regularizer=l2(weight_decay), name='fc1')(x)
        x = Dense(4096, activation='relu', W_regularizer=l2(weight_decay),
                  b_regularizer=l2(weight_decay), name='fc2')(x)
        x = Dense(classes, activation='softmax', W_regularizer=l2(weight_decay),
                  b_regularizer=l2(weight_decay), name='predictions')(x)

    # Ensure that the model takes into account
    # any potential predecessors of `input_tensor`.
    if input_tensor is not None:
        inputs = get_source_inputs(input_tensor)
    else:
        inputs = img_input
    # Create model.
    model = Model(inputs, x, name='vgg19')

    # load weights
    if weights == 'imagenet':
        if K.image_dim_ordering() == 'th':
            if include_top:
                weights_path = get_file('vgg19_weights_th_dim_ordering_th_kernels.h5',
                                        TH_WEIGHTS_PATH,
                                        cache_subdir='models')
            else:
                weights_path = get_file('vgg19_weights_th_dim_ordering_th_kernels_notop.h5',
                                        TH_WEIGHTS_PATH_NO_TOP,
                                        cache_subdir='models')
            model.load_weights(weights_path)
            if K.backend() == 'tensorflow':
                warnings.warn('You are using the TensorFlow backend, yet you '
                              'are using the Theano '
                              'image dimension ordering convention '
                              '(`image_dim_ordering="th"`). '
                              'For best performance, set '
                              '`image_dim_ordering="tf"` in '
                              'your Keras config '
                              'at ~/.keras/keras.json.')
                convert_all_kernels_in_model(model)
        else:
            if include_top:
                weights_path = get_file('vgg19_weights_tf_dim_ordering_tf_kernels.h5',
                                        TF_WEIGHTS_PATH,
                                        cache_subdir='models')
            else:
                weights_path = get_file('vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5',
                                        TF_WEIGHTS_PATH_NO_TOP,
                                        cache_subdir='models')
            model.load_weights(weights_path)
            if K.backend() == 'theano':
                convert_all_kernels_in_model(model)
    return model
