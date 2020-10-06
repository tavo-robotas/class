#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "turtlesim/Pose.h"

using namespace std;
const double PI = 3.14159265359;

ros::Publisher velocity_publisher;
ros::Subscriber pose_subscriber;
turtlesim::Pose turtlesim_pose;
turtlesim::Pose goal_pose;

const double x_min = 0.0;
const double y_min = 0.0;
const double x_max = 11.0;
const double y_max = 11.0;

void move(double speed, double distance, bool isForward);
void rotate(double angular_speed, double relative_angle, bool clockwise);
double deg2rad(double angle_in_degrees);
void setDesiredOrientation(double angle_in_radians);
double getDistance(double x1, double y1, double x2, double y2);
void poseCallback(const turtlesim::Pose::ConstPtr & pose_message);
void moveToGoal(turtlesim::Pose goal_pose, double distance_torelance);
void gridClean();

int main(int argc, char **argv)
{
      ros::init(argc, argv, "turtlesim_cleaner");
      ros::NodeHandle n;
      velocity_publisher = n.advertise<geometry_msgs::Twist>("turtle1/cmd_vel", 10);
      pose_subscriber = n.subscribe("/turtle1/pose", 10, poseCallback);
      ros::Rate loop_rate(0.5);

      // double speed;
      // double distance;
      // bool isForward;
      
      // double angle;
      // double angular_speed;
      // bool clockwise;

      // cout<<"greitis: ";
      // cin>>speed;
      // cout<<"atstumas: ";
      // cin>>distance;
      // cout<<"kryptis: ";
      // cin>>isForward;
      // move(speed, distance, isForward);

      // cout<<"greitis (deg/s): ";
      // cin>>angular_speed;
      // cout<<"kampas (deg):";
      // cin>>angle;
      // cout<<"krypts: ";
      // cin>>clockwise;
      // rotate(deg2rad(angular_speed), deg2rad(angle), clockwise);

      // setDesiredOrientation(deg2rad(120));
      // loop_rate.sleep();
      // setDesiredOrientation(deg2rad(-60));
      // loop_rate.sleep();
      // setDesiredOrientation(deg2rad(0));
      // goal_pose.x = 1;
      // goal_pose.y = 1;
      // goal_pose.theta = 0;
      // moveToGoal(goal_pose, 0.01);
      gridClean();
      loop_rate.sleep();

      ros::spin();
      return 0;

}

void moveToGoal(turtlesim::Pose goal_pose, double distance_tolerance)
{
    geometry_msgs::Twist vel_msg;
    ros::Rate loop_rate(10);
    do{
        vel_msg.linear.x = 1.5 * getDistance(turtlesim_pose.x, turtlesim_pose.y, goal_pose.x, goal_pose.y);
        vel_msg.linear.y = 0;
        vel_msg.linear.z = 0;
        
        vel_msg.angular.x = 0;
        vel_msg.angular.y = 0;
        vel_msg.angular.z = 4 * (atan2(goal_pose.y - turtlesim_pose.y , goal_pose.x - turtlesim_pose.x)-turtlesim_pose.theta);
        velocity_publisher.publish(vel_msg);
        ros::spinOnce();
        loop_rate.sleep();
    }while(getDistance(turtlesim_pose.x, turtlesim_pose.y, goal_pose.x, goal_pose.y) > distance_tolerance);
      vel_msg.linear.x = 0;
      vel_msg.angular.z = 0;
      velocity_publisher.publish(vel_msg);
}

void rotate(double angular_speed, double relative_angle, bool clockwise)
{
      geometry_msgs::Twist vel_msg;
      vel_msg.linear.x = 0;
      vel_msg.linear.y = 0;
      vel_msg.linear.z = 0;

      vel_msg.angular.x = 0;
      vel_msg.angular.y = 0;
      vel_msg.angular.z = (clockwise ? -abs(angular_speed) : abs(angular_speed));
      double current_angle = 0.0;
      double t0 = ros::Time::now().toSec();
      ros::Rate loop_rate(10);
      do{
            velocity_publisher.publish(vel_msg);
            double t1  = ros::Time::now().toSec();
            current_angle = angular_speed * (t1 - t0);
            ros::spinOnce();
            loop_rate.sleep();
            // ROS_INFO("\n\n\n ********SPINNING*********\n");
            // ROS_INFO_STREAM("current_angle: " << current_angle);
            // ROS_INFO_STREAM("relative_angle: " << relative_angle);
      }while(current_angle<=relative_angle);
      vel_msg.angular.z = 0;
      velocity_publisher.publish(vel_msg);
}

void moveBot(double speed , double distance, bool isForward)
{
    geometry_msgs::Twist vel_msg;
    vel_msg.linear.x = isForward ? abs(speed) : -abs(speed); 
    vel_msg.linear.y = 0;
    vel_msg.linear.z = 0;
    vel_msg.angular.x = 0;
    vel_msg.angular.y = 0;
    vel_msg.angular.z = 0;
    
    double t0 = ros::Time::now().toSec();
    double current_distance = 0;
    ros::Rate loop_rate(10);
    do{
        velocity_publisher.publish(vel_msg);
        double t1 = ros::Time::now().toSec();
        current_distance = speed * (t1 - t0);
        ros::spinOnce();
        loop_rate.sleep();
    }while (current_distance <= distance);
    //stop the cleaner 
    vel_msg.linear.x = 0;
    velocity_publisher.publish(vel_msg);
}

void gridClean(){
	ros::Rate loop(0.5);
	goal_pose.x=1;
	goal_pose.y=1;
	goal_pose.theta=0;
	moveToGoal(goal_pose, 0.01);
	loop.sleep();
	setDesiredOrientation(deg2rad(-15));
	loop.sleep();
	moveBot(4, 9, true);
	loop.sleep();
	rotate(deg2rad(30), deg2rad(90), false);
	loop.sleep();
	moveBot(4, 9, true);
	rotate(deg2rad(30), deg2rad(90), false);
	loop.sleep();
	moveBot(4, 1, true);
	rotate(deg2rad(30), deg2rad(90), false);
	loop.sleep();
	moveBot(4, 9, true);
	rotate(deg2rad(30), deg2rad(90), true);
	loop.sleep();
	moveBot(4, 1, true);
	rotate(deg2rad(30), deg2rad(90), true);
	loop.sleep();
	moveBot(4, 9, true);
	double distance = getDistance(turtlesim_pose.x, turtlesim_pose.y, x_max, y_max);
}

void poseCallback(const turtlesim::Pose::ConstPtr & pose_message)
{
      turtlesim_pose.x=pose_message->x;
      turtlesim_pose.y=pose_message->y;
      turtlesim_pose.theta=pose_message->theta;
}

void setDesiredOrientation(double desired_angle_in_rad)
{
      double relative_angle_radians = desired_angle_in_rad - turtlesim_pose.theta;
	bool clockwise = ((relative_angle_radians<0)?true:false);
	//cout<<desired_angle_radians <<","<<turtlesim_pose.theta<<","<<relative_angle_radians<<","<<clockwise<<endl;
	rotate (abs(relative_angle_radians), abs(relative_angle_radians), clockwise);
}

double getDistance(double x1, double y1, double x2, double y2)
{
    return sqrt(pow((x1-x2),2)+pow((y1-y2),2));
}

double deg2rad(double angle_in_degrees)
{
      return angle_in_degrees * PI/ 180;
}

