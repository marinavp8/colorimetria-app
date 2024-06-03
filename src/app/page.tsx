import Head from 'next/head';
import ImageUpload from '@/app/components/ImageUpload';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Colorimetría App</title>
      </Head>
      <ImageUpload />
    </div>
  );
}
