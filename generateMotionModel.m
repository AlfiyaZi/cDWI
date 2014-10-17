function motionModel = generateMotionModel(cineImageDir)
% Purpose: to read a series of short-axis DICOM images, detect left
% venticular myocardium in them and create a time model of transformation
cineImageFiles = dir ([cineImageDir '*I*.dcm']);
index = 1;
for cineImageFile = cineImageFiles'
    image = dicomread(fullfile(cineImageDir,cineImageFile.name));
    % Initiate the entire array that contains all the images from the first
    % image
    if index == 1
        cine = zeros (size(image,1), size(image,2), size(cineImageFiles,1));
    end
    cine(:,:,index) = image;
    index = index + 1;
end
% show a diff image in time in order to visualize cardiac quiescent phase
cineDiff = diff(cine,1,3);
figure,render(abs(cineDiff),[0 200]);
figure, render(cine);
entropies = zeros(1,size(cineDiff,3));
for i=1: size(cineDiff,3)
    entropies(i) = entropy(cineDiff(:,:,i));
end
figure, plot(entropies);
motionModel = image;
% collapse the image into a vector
cineCollapsed = reshape(cine,size(cine,1)*size(cine,2),size(cine,3));
end