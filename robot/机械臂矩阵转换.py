

class HandInEyeCalibration:
    def __init__(self, ):
        pass

    def get_points_robot(self, x_camera, y_camera, m):
        """
        相机坐标通过仿射矩阵变换取得机器坐标
        :param x_camera:
        :param y_camera:
        :return:
        """
        # m = self.get_m(STC_points_camera, STC_points_robot)

        robot_x = (m[0][0] * x_camera) + (m[0][1] * y_camera) + m[0][2]
        robot_y = (m[1][0] * x_camera) + (m[1][1] * y_camera) + m[1][2]
        return robot_x, robot_y

if __name__ == "__main__":
    a = HandInEyeCalibration()
    x_camera = 2202
    y_camera = 1618
    m = [[-0.000976969,   -0.013449341,   104.533955109],
         [0.013193269, -0.001274517, -251.564401739],]
    result = a.get_points_robot(x_camera, y_camera, m)
    tcp_cur = (80, -225)
    print(result[0] - tcp_cur[0], result[1] - tcp_cur[1])