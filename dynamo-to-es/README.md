* dynamoストリームでElasticsearchServiceに連携するモジュールのリリース

```
dynamo-to-es下の*をzip -r lambda.zip ./*して、lambdaにuploadする。
(DynamoのStreamを有効にしていること。IAMでlambda dynamo ESへのアクセス権限があること。ESでドメインを作って、インデックス/タイプを指定したデータ登録が行えること(PUT))

なおdeployモジュールは導入していない。
```
