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
overall_mean_combined, overall_std_combined = calc_overall_accuracy_and_std(combined_table)
overall_mean_separate, overall_std_separate = calc_overall_accuracy_and_std(separate_table)
overall_mean_sequential, overall_std_sequential = calc_overall_accuracy_and_std(sequential_table)

# Calculate per question metrics
mean_per_question_combined, std_per_question_combined = calc_group_accuracy_and_std(combined_table, 'Question Number')
mean_per_question_separate, std_per_question_separate = calc_group_accuracy_and_std(separate_table, 'Question Number')
mean_per_question_sequential, std_per_question_sequential = calc_group_accuracy_and_std(sequential_table, 'Question Number')

# Calculate per gender metrics
mean_per_gender_combined, std_per_gender_combined = calc_group_accuracy_and_std(combined_table, 'Gender')
mean_per_gender_separate, std_per_gender_separate = calc_group_accuracy_and_std(separate_table, 'Gender')
mean_per_gender_sequential, std_per_gender_sequential = calc_group_accuracy_and_std(sequential_table, 'Gender')

# Function that plots overall accuracy and standard deviations
def plot_overall_mean_and_std_dev(overall, separate, sequential, filename):
	plt.figure(figsize=(14, 7))
	plt.bar(['Combined', 'Separate', 'Sequential'], [overall[0], separate[0], sequential[0]],
		yerr=[overall[1], separate[1], sequential[1]], capsize=5)
	plt.ylabel('Mean and Standard Deviation')
	plt.title('Overall Mean and Standard Deviation')
	plt.savefig(filename)
	plt.close()

# Function that plots group accuracy and standard deviation
def plot_mean_and_std_dev_per_group(mean_combined, std_combined, mean_separate, std_separate, mean_sequential, std_sequential, group_name, filename):
	x = np.arange(len(mean_combined.index))
	width = 0.25

	fig, ax = plt.subplots(figsize=(14, 7))
	rects1 = ax.bar(x - width, mean_combined, width, label='Combined', yerr=std_combined, capsize=5)
	rects2 = ax.bar(x, mean_separate, width, label='Separate', yerr=std_separate, capsize=5)
	rects3 = ax.bar(x + width, mean_sequential, width, label='Sequential', yerr=std_sequential, capsize=5)

	ax.set_xlabel(group_name)
	ax.set_ylabel('Mean and Standard Deviation')
	ax.set_title(f'Mean and Standard Deviation per {group_name}')
	ax.set_xticks(x)
	ax.set_xticklabels(mean_combined.index)
	ax.legend()

	fig.tight_layout()
	plt.savefig(filename)
	plt.close()

# Function that plots mean accuracy and standard deviation per question per group
def plot_mean_and_std_dev_per_question_per_group(df_combined, df_separate, df_sequential, group_name, filename):
	group_entries = df_combined[group_name].unique()
	questions = df_combined['Question Number'].unique()

	combined_means = []
	combined_stds = []

	for entry in group_entries:
		combined_mean, combined_std = calc_group_accuracy_and_std(df_combined[df_combined[group_name] == entry], 'Question Number')

		combined_means.append(combined_mean)
		combined_stds.append(combined_std)

	num_questions = len(questions)
	num_groups = len(group_entries)
	total_bars = num_questions * num_groups

	x = np.arange(total_bars)
	width = 0.25

	fig, ax = plt.subplots(figsize=(30, 15))

	for i in range(num_groups):
		ax.bar(x[i::num_groups], combined_means[i], width, label=f'Combined, {group_name} {group_entries[i]}', yerr=combined_stds[i], capsize=5)

	ax.set_xlabel('Question Number')
	ax.set_ylabel('Mean and Standard Deviation')
	ax.set_title(f'Mean and Standard Deviation per Question per {group_name}')
	ax.set_xticklabels([f'Q{q}' for q in questions], rotation=90)
	ax.legend()

	fig.tight_layout()
	plt.savefig(filename)
	plt.close()

# Plot overall mean accuracy and standard deviation
plot_overall_mean_and_std_dev(
	(overall_mean_combined, overall_std_combined),
	(overall_mean_separate, overall_std_separate),
	(overall_mean_sequential, overall_std_sequential),
	'overall_mean_and_std_dev.png'
)

# Plot mean accuracy and standard deviation per question
plot_mean_and_std_dev_per_group(
	mean_per_question_combined, std_per_question_combined,
	mean_per_question_separate, std_per_question_separate,
	mean_per_question_sequential, std_per_question_sequential,
	'Question Number',
	'mean_and_std_dev_per_question.png'
)

# Plot mean accuracy and standard deviation per gender
plot_mean_and_std_dev_per_group(
	mean_per_gender_combined, std_per_gender_combined,
	mean_per_gender_separate, std_per_gender_separate,
	mean_per_gender_sequential, std_per_gender_sequential,
	'Gender',
	'mean_and_std_dev_per_gender.png'
)

# Plot mean accuracies and std devs for every individual question per gender
plot_mean_and_std_dev_per_question_per_group(
	combined_table,
	separate_table,
	sequential_table,
	'Gender',
	'mean_and_std_dev_per_question_per_gender.png'
)