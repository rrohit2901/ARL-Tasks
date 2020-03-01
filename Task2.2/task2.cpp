#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include<bits/stdc++.h>

#define step 3

using namespace std;
using namespace cv;

float dis(Point p1, Point p2, Point p3){
    float l,a,b;
    l = sqrt((p1.x-p2.x)*(p1.x-p2.x)+(p1.y-p2.y)*(p1.y-p2.y));
    a = sqrt((p3.x-p2.x)*(p3.x-p2.x)+(p3.y-p2.y)*(p3.y-p2.y));
    b = sqrt((p1.x-p3.x)*(p1.x-p3.x)+(p1.y-p3.y)*(p1.y-p3.y));
    float d = (4*l*l*b*b)-(a*a-b*b-l*l)*(a*a-b*b-l*l);
    d /= (4*l*l);
    d = sqrt(d);
    return d;
}

int main(){
    cout<<"Enter number of collisions expected between balls."<<flush;
    int c_ball;
    cin>>c_ball;
    Mat img = imread("task2.png",0);
    Mat img2(img.rows,img.cols,CV_8UC3,Scalar(0,0,0));
    Mat img3 = img2.clone();
    vector<Vec4i> lines;
    HoughLinesP(img, lines, 1, CV_PI/180, 50, 50, 10); 
    Vec4i l = lines[1];
    line( img2, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0,0,255), 1, CV_AA);
    float l_angle = atan((l[1]-l[3])/(l[0]-l[2]));
    //l_angle = l_angle*180/3.14;
    GaussianBlur( img, img, Size(9, 9), 2, 2 );
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    Canny( img, img, 50, 200, 3 );
    findContours( img, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    // for( int i = 0; i< contours.size(); i++ ){
    //     drawContours( img2, contours, i, Scalar(0,0,255), 2, 8, hierarchy, 0, Point() );
    // }
    float avg_rad;
    for(int i=0;i<contours.size();i++){
        avg_rad+=arcLength(contours[i],true);
    }
    cout<<contours.size()<<endl;
    avg_rad/=(contours.size()*3.14*2);
    cout<<"Average radius is:"<<avg_rad<<endl;
    float min_dis = INT_MAX;
    int index = 0;
    int m_centerx, m_centery;
    Point centers[contours.size()/2];
    for(int i=0;i<contours.size();i+=2){
        Moments M = moments(contours[i]);
        Point center;
        center.x = int(M.m10/M.m00);
        center.y = int(M.m01/M.m00); 
        float d = dis(Point(l[0],l[1]),Point(l[2],l[3]),center);
        centers[i] = center;
        if(d<min_dis){
            index = i;
            m_centerx = center.x;
            m_centery = center.y;
            min_dis = d;
        }
    }
    int count = 0;
    while(1){
        img2 = img3.clone();
        int rad = avg_rad, flag = 0;
        circle(img2, Point(m_centerx,m_centery), 25, Scalar(255,255,255), -1);
        m_centerx+= (int)(step * cos(l_angle));
        m_centery+= (int)(step * sin(l_angle)); 
        // cout<<m_centerx<<" "<<m_centery<<" "<<l_angle<<endl;
        line( img2, Point(m_centerx, m_centery), Point(m_centerx+ step * 10 * cos(l_angle), m_centery+ step * 10 * sin(l_angle)), Scalar(0,0,255), 1, CV_AA);
        if(m_centerx + 25 > img.cols){
            l_angle *= (180/3.14);
            l_angle = 180 - l_angle;
            l_angle *= (3.14/180);
        }
        if(m_centerx-25 < 0){
            l_angle *= (180/3.14);
            l_angle = 180 - l_angle;
            l_angle *= (3.14/180);
        }
        if(m_centery + 25 > img.rows){
            l_angle *= (180/3.14);
            l_angle = 45 + l_angle;
            l_angle *= (3.14/180);
        }
        if(m_centery-25 < 0){
            l_angle *= (180/3.14);
            l_angle = 45 + l_angle;
            l_angle *= (3.14/180);
        }
        for(int i=0;i<contours.size();i+=2){
            if(i==index){
                centers[i] = Point(m_centerx,m_centery);
                continue;
            }
            // Moments M = moments(contours[i]);
            // Point center;
            // center.x = int(M.m10/M.m00);
            // center.y = int(M.m01/M.m00);
            circle(img2, centers[i], 25, Scalar(0,0,255));
            float d = sqrt((centers[i].x-m_centerx)*(centers[i].x-m_centerx)+(centers[i].y-m_centery)*(centers[i].y-m_centery));
            if(d<2*25){
                count += 1;
                cout<<"collision between "<<index/2<<" and "<<i/2<<endl;
                index = i;
                m_centerx = centers[i].x;
                m_centery = centers[i].y;
                break;
            }
        }
        if(count == c_ball){
            break;
        }
        namedWindow("window",WINDOW_NORMAL);
        namedWindow("original",WINDOW_NORMAL);
        imshow("original",img);
        imshow("window",img2);
        waitKey(10);
        waitKey(10);
    }
    return 0;
}
