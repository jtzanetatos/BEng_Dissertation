#include <iostream>
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/imgproc.hpp>
#include <opencv4/opencv2/core.hpp>
#include <cstdlib>

using namespace std;

// pair <cv::Mat, cv::Mat> imBackSub(cv::Mat bg, cv::Mat fr, int thresh) {
//   // Initialize output par
//   pair <cv::Mat, cv::Mat> out;
//   // Initialize background subtraction frame
//   cv::Mat fr_diff, bg_bw, fr_bw, fg;
//
//
//   // Convert input frames into Grayscale
//   cv::cvtColor(fr, fr_bw, cv::COLOR_BGR2GRAY);
//   cv::cvtColor(bg, bg_bw, cv::COLOR_BGR2GRAY);
//
//   // Subtract background from foreground
//   fr_diff = fr_bw - bg_bw;
//
//   // Loop through Subtracted frame model & apply high pass filtering
//   for(int i=0; i < fr.cols; i++) {
//     for(int j=0; j < fr.rows; j++) {
//       if (fr_diff[i][j] > thresh)
//           fg[i][j] = fr_bw[i][j];
//       else
//           fg[i][j] = 0;
//     }
//   }
//
//   // Update background frame for next iteration
//   bg_bw = fr_bw;
//
//   // Set output pairs
//   out.first = fg;
//   out.second = bg_bw;
//
//   return out;
// }

cv::Mat contour(cv::Mat fg, int ns1, int nn) {
        // Initialize output frame
        cv::Mat fgc;

        // Construct morphological object
        cv::Mat sel = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(ns1, ns1));

        // Apply median filter
        for (int i=1; i < nn*nn; i += 2)
                cv::medianBlur(fg, fgc, i);

        // Apply morphological operation on filtered frame
        cv::morphologyEx(fgc, fgc, cv::MORPH_CLOSE, sel);

        // Return frame
        return fgc;
}



int main(int argc, char **argv)
{
        // Create videoCaputre object
        cv::VideoCapture cap;

        if(argc == 2)
                cap.open(argv[1]);
        else
                cap.open(0);

        // Check if camera/video feed opened successfully
        if( !cap.isOpened() ) {
                printf("Error opening video stream or file.\n");
                exit(1);
        }

        // Initialize background & current frame
        cv::Mat bg, fr;

        // Read first frame as Background
        cap >> bg;

        // Loop through video stream/file
        while(1) {

                // Read current frame
                cap >> fr;

                // If frame is empy, break
                if ( fr.empty() ) {
                        printf("End of video file/stream.\n");
                        break;
                }

                // Show input frame
                cv::imshow("Frame", fr);

                int keyboard = cv::waitKey(30);
                if (keyboard == 'q' || keyboard == 27)
                        break;

        }

        // Clean up capture object
        cap.release();

        // Clean up windows
        cv::destroyAllWindows();

        return 0;
}
