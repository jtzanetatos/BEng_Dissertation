#include <iostream>
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/imgproc.hpp>
#include <opencv4/opencv2/core.hpp>
#include <cstdlib>

using namespace std;

// pair <cv::Mat, cv::Mat> imBackSub(cv::Mat bg, cv::Mat fr, int thresh) {
//         // Initialize output par
//         pair <cv::Mat, cv::Mat> out;
//         // Initialize background subtraction frame
//         cv::Mat fr_diff, bg_bw, fr_bw, fg;
//
//
//         // Convert input frames into Grayscale
//         cv::cvtColor(fr, fr_bw, cv::COLOR_BGR2GRAY);
//         cv::cvtColor(bg, bg_bw, cv::COLOR_BGR2GRAY);
//
//         // Subtract background from foreground
//         cv::absdiff(fr_bw, bg_bw, fr_diff);
//
//         // Assert only char type images
//         CV_Assert(fg.depth() == CV_8UC3);
//
//         int channels = fg.channels();
//
//         int nRows = fg.rows;
//         int nCols = fg.cols * channels;
//
//         if ( fg.isContinuous() ) {
//                 nCols *= nRows;
//                 nRows = 1;
//         }
//
//         int i, j;
//         uchar *pin, *pout;
//
//         for( i = 0; i < nRows; ++i) {
//
//                 pin = fr_diff.ptr<uchar>(i);
//                 pout = fg.ptr<uchar>(i);
//                 for( j = 0; i < nCols; ++j) {
//                         if( fr_diff[pin[j]] > thresh ) {
//                                 pout[j] = fr_diff[pout[j]];
//
//                         }
//                         else {
//                                 pout[j] = 0;
//                         }
//                 }
//         }
//         // Loop through Subtracted frame model & apply high pass filtering
//         // for(int i=0; i < fr.cols; i++) {
//         //         for(int j=0; j < fr.rows; j++) {
//         //                 if (fr_diff[i][j] > thresh)
//         //                         fg.at<uchar>(i, j) = fr_bw.at<uchar>(i, j);
//         //                 else
//         //                         fg.at<uchar>(i, j) = 0;
//         //         }
//         // }
//
//         // Update background frame for next iteration
//         bg_bw = fr_bw;
//
//         // Set output pairs
//         out.first = fg;
//         out.second = bg_bw;
//
//         return out;
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

cv::Mat clrCnv(cv::Mat fr, cv::Mat fgc) {

        // Assert input frame's dtype
        CV_Assert(fr.depth() == CV_8U);

        int channels = fr.channels();
        int nRows = fr.rows;
        int nCols = fr.cols * channels;

        if( fr.isContinuous() ) {
                nCols *= nRows;
                nRows = 1;
        }

        // Convert RGB/BGR array into vector & split colour channels
        std::vector<cv::Mat> ch_split;

        cv::split(fr, ch_split);

        cv::Mat fgcRGB = cv::Mat( fr.rows, fr.cols, CV_8UC3, CV_RGB(1,1,1) );

        uchar* p;
        for (int i = 0; i < fr.channels(); i++) {

        }

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
        cv::Mat bg, fr, fgcRGB;

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


                // Convert frame from Grayscale to RGB/BGR
                // cv::mutliply(fr, fgc, fgcRGB);

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
