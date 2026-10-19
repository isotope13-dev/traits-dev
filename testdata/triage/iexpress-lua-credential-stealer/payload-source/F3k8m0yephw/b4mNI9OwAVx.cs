using System.Text;

namespace F3k8m0yephw;

public abstract class b4mNI9OwAVx
{
	public abstract byte[] GetBytes();

	public override string ToString()
	{
		int num = 0;
		StringBuilder stringBuilder = default;
		do
		{
			if (num == 2)
			{
				stringBuilder.AppendFormat("{0}:", GetType().Name);
				num = 3;
			}
			if (num == 3)
			{
				stringBuilder.AppendLine();
				num = 4;
			}
			if (num == 1)
			{
				stringBuilder = new StringBuilder();
				num = 2;
			}
			if (num == 0)
			{
				num = 1;
			}
		}
		while (num != 4);
		return stringBuilder.ToString();
	}
}
