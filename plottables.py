import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load spreadsheets
separate_table = pd.read_excel('separate_table.xlsx')
sequential_table = pd.read_excel('sequential_table.xlsx')
combined_table = pd.concat([separate_table, sequential_table])

# Function that calculates the overall mean accuracy and standard deviation
def calc_overall_accuracy_and_std(df):
	overall_accuracy = (df['Is Correct'] == 'Correct').mean()
	overall_std = (df['Is Correct'] == 'Correct').std()
	return overall_accuracy, overall_std

# Function that calculates group mean accuracy and standard deviation
def calc_group_accuracy_and_std(df, group):
	accuracy = df.groupby(group)['Is Correct'].apply(lambda x: (x == 'Correct').mean())
	std = df.groupby(group)['Is Correct'].apply(lambda x: (x == 'Correct').std())
	return accuracy, std

# Calculate overall metrics
overall_accuracy_combined, overall_std_combined = calc_overall_accuracy_and_std(combined_table)
overall_accuracy_separate, overall_std_separate = calc_overall_accuracy_and_std(separate_table)
overall_accuracy_sequential, overall_std_sequential = calc_overall_accuracy_and_std(sequential_table)

# Calculate per question metrics
accuracy_per_question_combined, std_per_question_combined = calc_group_accuracy_and_std(combined_table, 'Question Number')
accuracy_per_question_separate, std_per_question_separate = calc_group_accuracy_and_std(separate_table, 'Question Number')
accuracy_per_question_sequential, std_per_question_sequential = calc_group_accuracy_and_std(sequential_table, 'Question Number')

# Calculate per role metrics
accuracy_per_role_combined, std_per_role_combined = calc_group_accuracy_and_std(combined_table, 'Role')
accuracy_per_role_separate, std_per_role_separate = calc_group_accuracy_and_std(separate_table, 'Role')
accuracy_per_role_sequential, std_per_role_sequential = calc_group_accuracy_and_std(sequential_table, 'Role')

# Calculate per temperature metrics
accuracy_per_temp_combined, std_per_temp_combined = calc_group_accuracy_and_std(combined_table, 'Temperature')
accuracy_per_temp_separate, std_per_temp_separate = calc_group_accuracy_and_std(separate_table, 'Temperature')
accuracy_per_temp_sequential, std_per_temp_sequential = calc_group_accuracy_and_std(sequential_table, 'Temperature')

# Function that plots overall accuracy and standard deviations
def plot_overall_accuracy(overall, separate, sequential, filename):
	plt.figure(figsize=(10, 6))
	plt.bar(['Combined', 'Separate', 'Sequential'], [overall[0], separate[0], sequential[0]],
		yerr=[overall[1], separate[1], sequential[1]], capsize=5)
	plt.ylabel('Mean Accuracy')
	plt.title('Overall Mean Accuracy and Standard Deviation')
	plt.savefig(filename)
	plt.close()

# Function that plots group accuracy and standard deviation
def plot_group_accuracy(accuracy_combined, std_combined, accuracy_separate, std_separate, accuracy_sequential, std_sequential, group_name, filename):
	x = np.arange(len(accuracy_combined.index))
	width = 0.25

	fig, ax = plt.subplots(figsize=(14, 7))
	rects1 = ax.bar(x - width, accuracy_combined, width, label='Combined', yerr=std_combined, capsize=5)
	rects2 = ax.bar(x, accuracy_separate, width, label='Separate', yerr=std_separate, capsize=5)
	rects3 = ax.bar(x + width, accuracy_sequential, width, label='Sequential', yerr=std_sequential, capsize=5)

	ax.set_xlabel(group_name)
	ax.set_ylabel('Accuracy')
	ax.set_title(f'Mean Accuracy per {group_name} and Standard Deviation')
	ax.set_xticks(x)
	ax.set_xticklabels(accuracy_combined.index)
	ax.legend()

	fig.tight_layout()
	plt.savefig(filename)
	plt.close()

# Function that plots mean accuracy and standard deviation per question per group
def plot_accuracy_per_question_group(df_combined, df_separate, df_sequential, group):
	group_entries = df_combined[group].unique()
	questions = df_combined['Question Number'].unique()

	for entry in group_entries:
		accuracy_combined, std_combined = calc_group_accuracy_and_std(df_combined[df_combined[group] == entry], 'Question Number')
		accuracy_separate, std_separate = calc_group_accuracy_and_std(df_separate[df_separate[group] == entry], 'Question Number')
		accuracy_sequential, std_sequential = calc_group_accuracy_and_std(df_sequential[df_sequential[group] == entry], 'Question Number')

		plot_group_accuracy(accuracy_combined, std_combined, accuracy_separate, std_separate, accuracy_sequential, std_sequential, f'Question Number ({group}: {entry})', f'plot_{group}_{entry}.png')

# Plot overall mean accuracy and standard deviation
plot_overall_accuracy(
	(overall_accuracy_combined, overall_std_combined),
	(overall_accuracy_separate, overall_std_separate),
	(overall_accuracy_sequential, overall_std_sequential),
	'overall_accuracy.png'
)

# Plot mean accuracy and standard deviation per question
plot_group_accuracy(
	accuracy_per_question_combined, std_per_question_combined,
	accuracy_per_question_separate, std_per_question_separate,
	accuracy_per_question_sequential, std_per_question_sequential,
	'Question Number',
	'accuracy_per_question.png'
)

# Plot mean accuracy and standard deviation per role
plot_group_accuracy(
	accuracy_per_role_combined, std_per_role_combined,
	accuracy_per_role_separate, std_per_role_separate,
	accuracy_per_role_sequential, std_per_role_sequential,
	'Role',
	'accuracy_per_role.png'
)

# Plot mean accuracy and standard deviation per temperature
plot_group_accuracy(
	accuracy_per_temp_combined, std_per_temp_combined,
	accuracy_per_temp_separate, std_per_temp_separate,
	accuracy_per_temp_sequential, std_per_temp_sequential,
	'Temperature',
	'accuracy_per_temperature.png'
)

# Plot mean accuracies and  std devs for every individual question per role
plot_accuracy_per_question_group(combined_table, separate_table, sequential_table, 'Role')

# Plot mean accuracies and std devs for every individual question per temperature
plot_accuracy_per_question_group(combined_table, separate_table, sequential_table, 'Temperature')
