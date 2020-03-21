from model import Model


# Constants
DATA_FOLDER='data',
CODE_FILE_LIST='code_list.txt'
SEQUENCE_DB="sequeces.db"
SEQ_LENGTH=40
BATCH_SIZE=32
VOCAB_SIZE=128
STEPS_PER_EPOCH=None
STEPS_PER_EPOCH_VALIDATION=None
TRAIN_SIZE = 33274973
VALIDATION_SIZE = 4150122
TEST_SIZE = 3870306
EPOCHS=5

# Initalizing the Class Model
model = Model(DATA_FOLDER=DATA_FOLDER,
			  CODE_FILE_LIST=CODE_FILE_LIST, 
			  SEQUENCE_DB=SEQUENCE_DB,
			  SEQ_LENGTH=SEQ_LENGTH,
			  BATCH_SIZE=BATCH_SIZE,
			  VOCAB_SIZE=VOCAB_SIZE,
			  STEPS_PER_EPOCH=None,
			  STEPS_PER_EPOCH_VALIDATION=None,
			  TRAIN_SIZE=TRAIN_SIZE,
			  VALIDATION_SIZE=VALIDATION_SIZE,
			  TEST_SIZE=TEST_SIZE,
			  EPOCHS=EPOCHS)

# Generating all the file list present in the Chromium codebase
model.generate_code_list(force=False)

# Building Sequences for training
model.build_sequences(force=False)

# Building the model and training it
model.build_model()