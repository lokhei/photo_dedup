    # result = {'images/20190725_195942.jpg': ['images/20190725_195944.jpg', 'images/20190725_195945.jpg', 'images/20190725_195946.jpg', 'images/20190725_195947.jpg', 'images/20190725_195949.jpg'], 'images/20190806_152610.jpg': ['images/20190806_152611.jpg'], 'images/20190806_153256.jpg': ['images/20190806_153259.jpg'], 'images/20190806_153445.jpg': ['images/20190806_153448.jpg', 'images/20190806_153449.jpg'], 'images/20190806_153531.jpg': ['images/20190806_153535.jpg'], 'images/20190806_153542.jpg': ['images/20190806_153543.jpg'], 'images/received_1238167046384879.jpeg': ['images/received_591336128061108.jpeg'], 'images/received_1446293368851368.jpeg': ['images/received_2248545758791910.jpeg', 'images/received_636852053391041.jpeg'], 'images/received_1669270329874592.jpeg': ['images/received_1860228334122433.jpeg', 'images/received_2455974407980752.jpeg', 'images/received_474708353362732.jpeg', 'images/received_700614207066273.jpeg'], 'images/received_2397690047169942.jpeg': ['images/received_853499358368703.jpeg'], 'images/received_2449826415245875.jpeg': ['images/received_358791084799482.jpeg'], 'images/received_2951191014943318.jpeg': ['images/received_880075679029306.jpeg'], 'images/received_329925327884101.jpeg': ['images/received_472849746881376.jpeg'], 'images/received_361478017814576.jpeg': ['images/received_971134336552092.jpeg'], 'images/received_375343243114685.jpeg': ['images/received_498372267605590.jpeg'], 'images/received_387161685151538.jpeg': ['images/received_469246037193848.jpeg', 'images/received_477885279656890.jpeg'], 'images/received_392299164820990.jpeg': ['images/received_923907671291694.jpeg'], 'images/received_501874913919241.jpeg': ['images/received_713087319141907.jpeg']}




def find_clusters(image_folder, eps=0.5, min_samples=2):
    
    features_list = []
    image_paths = []

    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            features = extract_features(image_path, model)
            features_list.append(features[0])
            image_paths.append(image_path)

    features_array = np.array(features_list)
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(features_array)
    clusters = {}

    for idx, label in enumerate(clustering.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(image_paths[idx])

    return clusters