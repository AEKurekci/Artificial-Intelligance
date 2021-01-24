#title: "20/21 Data Science Final Homework"
#author: "Ali Emre Kürekci"
#date: "15 01 2021"

#####WARNING#####
#Please before running, set the session working directory via Session -> Set 
#   Working Directory -> Choose Directory and select where your dataset or 
#   if you give data link set the where you want to work and save the plot results

#binary classification ml pipeline

#data_url: the url of the data set

#label_name: the class response name in character format

#prepro_method: pre-process method type 'scale', 'range', center etc.

#positive_class: postive class of labels for confusion matrix

#is_install_lib: if user do not need to install required libs s/he can give it 
#       as FALSE default is TRUE

#train_prob: train rate for splitting. default is 0.8

#skimmed_cols: user can give skimmed columns number for explorating data more

#plot_type: "box" or "density" options for plot chart. Default is "box"

#imputation_method: imputation method for missing data. knnImpute or bagImpute,
#       default is knnImpute

#numeric_as_categorical: there may be categorical columns with specified in numeric
#       format such as 1, 2, 3 for unhappy, normal and happy but in some preprocess
#       application r need to ignore categorical columns. User can give these column 
#       numbers by this option

#delete_col_nums:If you can not interest in some columns, you can delete by giving
#       column numbers of them

#use_one_hot_encode:If you want to use one-hot encoding process for character 
#       categorical variables, you should give it as TRUE and default is TRUE

#missing_method: If you apply missing value imputation with the help of mice 
#       library, you can give missing method. Default is NULL

#ignore_missing: You can give ignoring column numbers whilte imputing missing 
#       values. Default is NULL

#noise_type:Noise filter type while using NoiseFilterR library. Options are 
#       "remove" or "hybrid", default is NULL

#percv_over: perc.over value for class balancing

#percv_under: perc.under value for class balancing

#train_methods: models that you want to use in ml pipeline. Default is
#       list('knn', 'lda', 'rf', 'naive_bayes', 'rpart')

#model_ind_for_importance: Model index of train_methods for exploring feature 
#       importance. Default is 1

main <- function(data_url, label_name, prepro_method, positive_class, 
                 is_install_libs = TRUE, train_prob = 0.8, skimmed_cols = NULL, 
                 plot_type = "box", imputation_method = 'knnImpute', 
                 numerics_as_categorical = NULL,  
                 delete_col_nums = NULL, use_one_hot_encode = TRUE, 
                 missing_method = NULL, ignore_missing = NULL, noise_type = NULL, 
                 perc_over = NULL, perc_under=NULL, train_methods = 
                   list('knn', 'lda', 'rf', 'naive_bayes', 'rpart'),
                 model_ind_for_importance = 1){
  install_functions <- function(){
    install.packages(c('caret', 'skimr', 'RANN', 'randomForest', 'fastAdaboost', 
                       'gbm', 'xgboost', 'caretEnsemble', 'C50', 'earth', 'imbalance',
                       'DMwR', 'VIM', 'mice', 'NoiseFiltersR', 'kernlab'))
    
  }
  if(is_install_libs){
    print("Installing required packages")
    install_functions() 
  }
  # Load the caret package
  library(caret)
  print("Reading data")
  data <- read.csv(as.character(data_url))
  if(!is.null(delete_col_nums)){
    print("Deleting the given columns")
    data <<- data[, -delete_col_nums] 
  }
  
  # Structure of the dataframe
  str(data)
  
  col_num <- ncol(data)
  label_name_col <- c(label_name)
  
  #complete missing
  complete_missing <- function(d){
    library(mice)
    library(VIM)
    sapply(d, function(x) sum(is.na(x)))
    summary(d)
    
    mice_plot <- aggr(d, col=c('navyblue','red'), 
                      numbers=TRUE,labels=names(d), 
                      ylab=c("Missing data", "Pattern"))
    
    imp<-mice(d, meth=missing_method, ignore = ignore_missing)
    return(complete(imp))
  }
  if(!is.null(missing_method)){
    print("Completing missing values with the given method")
    data <- complete_missing()
    sapply(data, function(x) sum(is.na(x)))
  }
  #Noise filtering
  noise_filter <- function(d, n_type){
    library(ggplot2)
    library(NoiseFiltersR)
    for(i in 1:ncol(d)){
      if(typeof(d[,i]) == "character" || typeof(d[,i]) == "logical"){
        d[,i] = as.factor(d[,i])
      }
    }
    out <- hybridRepairFilter(d, noiseAction = as.character(n_type))
    summary(out, explicit = TRUE)
  }
  if(!is.null(noise_type)){
    print("applying noise filter")
    noise_filter(data, noise_type)
  }
  #Smoting
  smote_data <- function(d){
    library(imbalance)
    library(DMwR)
    
    smotedata <- d[, c(1:ncol(d))]
    for(i in 1:ncol(smotedata)){
      if(typeof(smotedata[,i]) == "character" || typeof(smotedata[,i]) == "logical"){
        smotedata[,i] = as.factor(smotedata[,i])
      }
    }
    temp_label <- paste(label_name, " ~ ." )
    temp_data <- SMOTE(as.formula(temp_label),data = smotedata, perc.over = perc_over, 
                  perc.under=perc_under)
    str(temp_data)
    return(temp_data)
  }
  if(!is.null(perc_under) && !is.null(perc_over)){
    print("Data is balancing")
    data <- smote_data(data)
  }
  
  #Data Partition
  print("Data is splitting as train and test")
  data_split = function(d, tr_prob, lb_name){
    set.seed(100)
    label_col_num <<- which(colnames(d) == lb_name)
    label_col_num
    
    # Step 1: Get row numbers for the training data
    trainRowNumbers <<- createDataPartition(d[,label_col_num], p=tr_prob, 
                                              list=FALSE)
    
    # Step 2: Create the training  dataset
    trainData <<- d[trainRowNumbers,]
    
    # Step 3: Create the test dataset
    testData <<- d[-trainRowNumbers,]
    
    # Store X and Y for later use.
    x <<- trainData[, -label_col_num]
    
    y <<- trainData[,label_col_num]
    
  }
  data_split(data, train_prob, label_name)
  
  #Descriptive statistic
  skimm_fn <- function(tr_data){
    library(skimr)
    library(rlang)
    skimmed <- skimr::skim(tr_data)
    skimmed[, skimmed_cols]
  }
  if(!is.null(skimmed_cols)){
    print("Descriptive statistic")
    skimm_fn(trainData)
  }  
  # Creating imputation model on the training data
  prep_miss <- function(){
    if(!is.null(numerics_as_categorical)){
      preProcess_missingdata_model <<- preProcess(trainData[, -numerics_as_categorical],
                                               method=imputation_method)
    }else{
      preProcess_missingdata_model <<- preProcess(trainData, method=imputation_method)
    }
    preProcess_missingdata_model
    
    #ensuring there is not any NA value
    library(RANN)
    anyNA(trainData)
    trainData <<- predict(preProcess_missingdata_model, newdata = trainData)
    anyNA(trainData)
  }
  
  if(!is.null(imputation_method)){
    print("Imputation for missing values")
    prep_miss()
  }
  
  #One-hot Encoding
  temp_label <- as.formula(paste(label_name, " ~ ." ))
  dummies_model <- NULL
  one_hot_encode <- function(){
    dummies_model <<- dummyVars(temp_label, data=trainData)
    trainData_mat <- predict(dummies_model, newdata = trainData)
    # # Convert to dataframe
    trainData <<- data.frame(trainData_mat)
    
    # # See the structure of the new dataset
    str(trainData)
  }
  if(use_one_hot_encode){
    print("One hot encoding")
    one_hot_encode()
  }

  print("Preprocessing continues")
  preProcess_range_model <- preProcess(trainData, method=prepro_method)
  trainData <- predict(preProcess_range_model, newdata = trainData)
  
  col_num <- ncol(trainData)
  
  # Append the Y variable
  trainData[,label_name] <- y
  print("Minimum and maximum values for all columns")
  apply(trainData[, 1:col_num], 2, FUN=function(x){c('min'=min(x), 'max'=max(x))})
  
  visualize_feature <- function(){
    label_col_num <- (which(colnames(trainData) == label_name))
    jpeg("rFeaturePlot.jpg", width = 600, height = 600)
    p <- featurePlot(x = trainData[, -label_col_num], 
                y = as.factor(trainData[, label_col_num]), 
                plot = plot_type,
                strip=strip.custom(par.strip.text=list(cex=.7)),
                scales = list(x = list(relation="free"), 
                              y = list(relation="free")))
    print(p)
    dev.off()
  }
  print("Visualization for features")
  visualize_feature()
  
  print("Models are running")
  model_run <- function(m){
    set.seed(100)
    label_col_num <- (which(colnames(trainData) == label_name))
    created_model = train(trainData[,-label_col_num], trainData[,label_col_num], 
                          method=as.character(m))
    return(created_model)
  }
  
  models <- list()
  for(i in 1:length(train_methods)){
    c_model = model_run(train_methods[i])
    models[[length(models) + 1]] <- c_model
  }
  
  feat_importance <- function(){
    jpeg("modelAccuracyWithMetric.jpg", width = 600, height = 600)
    p <- plot(models[[as.numeric(model_ind_for_importance)]], 
              main=paste("Model Accuracies with", 
                         train_methods[[as.numeric(model_ind_for_importance)]]))
    print(p)
    dev.off()
    varimp_knn <- varImp(models[[as.numeric(model_ind_for_importance)]])
    jpeg("featureImportanceGraph.jpg", width = 600, height = 600)
    p <- plot(varimp_knn, main=paste("Variable Importance with ", 
                                     train_methods[[as.numeric(model_ind_for_importance)]]))
    print(p)
    dev.off()
  }
  if(as.numeric(model_ind_for_importance) <= length(models)){
    print("Feature importance chart for the given model")
    feat_importance()
  }
  
  testing <- function(test_d){
    if(!is.null(imputation_method)){
      testData2 <<- predict(preProcess_missingdata_model, test_d) 
      testData3 <<- predict(dummies_model, testData2)
      testData4 <<- predict(preProcess_range_model, testData3)
    }else{
      testData3 <<- predict(dummies_model, test_d)
      testData4 <<- predict(preProcess_range_model, testData3)
    }
    
  }
  print("Test set is preparing")
  testing(testData)
  
  see_conf <- function(m, pos_class){
    fitted <- predict(m, testData4)
    sel_positive <- pos_class
    label_col_num <- (which(colnames(testData) == label_name))
    confusionMatrix(reference = testData[,label_col_num], data = fitted, mode='everything', 
                    positive=sel_positive)
  }
  print("==CONFUSION MATRIX==")
  for(i in 1:length(models)){
    temp_conf <- see_conf(models[[i]], positive_class)
    print(paste(train_methods[i], ' CONFUSION MATRIX'))
    print(temp_conf)
  }
  
  compare_list <- list()
  for(i in 1:length(train_methods)){
    compare_list[[train_methods[[i]]]] <- models[[i]]
  }
  print("Comparing Models")
  # Compare model performances using resample()
  models_compare <- resamples(compare_list)
  
  # Summary of the models performances
  summary(models_compare)
  
  # Draw box plots to compare models
  scales <- list(x=list(relation="free"), y=list(relation="free"))
  jpeg("modelComparing.jpg", width = 600, height = 600)
  p <- bwplot(models_compare, scales=scales)
  print(p)
  dev.off()
}

main(data_url = "./online_shoppers_intention.csv", label_name = "Revenue", 
     is_install_libs = FALSE, numerics_as_categorical = c(11:14), 
     prepro_method = 'range', perc_over = 200, perc_under=150, 
     skimmed_cols = c(1:5, 9:11, 13, 15), positive_class = 'TRUE')

# Another example with Orange Dataset
#main(data_url = 'https://raw.githubusercontent.com/selva86/datasets/master/orange_juice_withmissing.csv', 
#     label_name = "Purchase", positive_class = "MM", 
#     is_install_libs = FALSE, 
#     prepro_method = 'range', perc_over = 200, perc_under=150, 
#     skimmed_cols = c(1:5, 9:11, 13, 15))

