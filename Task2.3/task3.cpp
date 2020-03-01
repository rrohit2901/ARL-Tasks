#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/objdetect/objdetect.hpp"

#include<bits/stdc++.h>

using namespace std;
using namespace cv;

int main(){
	VideoCapture cap(0);
    String face_cascade_name = "haarcascade_frontalface_alt.xml";
    CascadeClassifier face_cascade;
	if(!cap.isOpened())
		return -1;
    if( !face_cascade.load( face_cascade_name ) ){ 
        cout<<"--(!)Error loading\n"<<endl;
        return -1;
    }
    int count=0, flag=0;    
    Point o_center;
    vector<Point>pt;
    srand(time(0));
	while(1){
		Mat img, img2;
		cap>>img;
        if(count==0){
            o_center.x = img.rows/2;
            o_center.y = img.cols/2;
        }
        count++;
        Mat img3(img.rows,img.cols,CV_8UC3,Scalar(196,166,16));
        circle(img3, o_center, 25, Scalar(16,196,196), -1, 8, 0);
        if(flag==1){
            for(auto i = pt.begin(); i != pt.end();i+=4){
                if(((i+1)->x)>0){
                    Point pt1,pt2;
                    i->x -= 10;
                    (i+1)->x -= 10;
                    (i+2)->x -= 10;
                    (i+3)->x -= 10;
                    pt1 = *i;
                    pt2 = *(i+1);
                    rectangle(img3, pt1, pt2, Scalar(11,94,24), -1);
                    pt1 = *(i+2);
                    pt2 = *(i+3);
                    rectangle(img3, pt1, pt2, Scalar(11,94,24), -1);
                    if(o_center.x+25 > (i->x) && o_center.x-25 < (i+1)->x){
                        if(o_center.y+25 > (i->y) || o_center.y-25 < (i+2)->y){
                            cout<<"---(!)GAME OVER(!)---"<<endl;
                            return 0;
                        }
                    }
                }
                else{
                    if(count%25==0)
                        flag=0;
                }
            }
        }
        if(flag==0){
            Point pt1,pt2;
            int a = 3*img.rows/7;
            int h1 = rand()%a, h2 = rand()%a;
            pt1.y = img.rows-h1;
            pt1.x = img.cols;
            pt2.y = img.rows;
            pt2.x = img.cols+50;
            pt.push_back(pt1);
            pt.push_back(pt2);
            rectangle(img3, pt1, pt2, Scalar(11,94,24), -1);
            pt1.y = h2;
            pt1.x = img.cols;
            pt2.y = 0;
            pt2.x = img.cols+50;
            pt.push_back(pt1);
            pt.push_back(pt2);
            rectangle(img3, pt1, pt2, Scalar(11,94,24), -1);
            flag=1;
        }
        cvtColor(img,img2,CV_BGR2GRAY);
        equalizeHist(img2,img2);
        vector<Rect> faces;
        face_cascade.detectMultiScale( img2, faces, 1.1, 2, 0|CV_HAAR_SCALE_IMAGE, Size(30,30));
        // cout<<faces.size()<<endl;
        int index;
        for(size_t i=0;i<faces.size();i++){
            Point center( faces[i].x + faces[i].width*0.5,faces[i].y + faces[i].height*0.5);
            ellipse( img, center, Size( faces[i].width*0.5, faces[i].height*0.5), 0, 0, 360, Scalar(0,0,255), 4, 8, 0);
            int max = INT_MIN;
            if(faces[i].width>max){
                max = faces[i].width;
                index = i; 
            }
        }
        if(!faces.empty()){
            Point center( faces[index].x + faces[index].width*0.5,faces[index].y + faces[index].height*0.5);
            if(center.x<3*img.cols/7 && o_center.x-30>0){
                o_center.x-=5;
            }
            else if(center.x>4*img.cols/7 && o_center.x+30<img.cols){
                o_center.x+=5;
            }
            if(center.y<img.rows/2 && o_center.y>30){
                o_center.y-=5;
            }
            else if(center.y>img.rows/2 && o_center.y+30<img.rows){
                o_center.y+=5;
            }
        }
        namedWindow("window",WINDOW_NORMAL);
        namedWindow("images",WINDOW_NORMAL);
        imshow("images",img3);
        imshow("window",img);
        waitKey(10);
        waitKey(10);
    }
    return 0;
}